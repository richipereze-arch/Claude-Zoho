"""Flujo de carga reanudable: plan → (búsquedas MCP) → classify → aprobación → (escritura MCP) → record → verify.

Cada lote vive en runs/<batch_id>/ (carpeta ignorada por git: contiene datos personales).
"""
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from . import dedup, mapping, normalize as n
from .schema import Schema, mask, SCHEMA_DIR

CHUNK = 100  # máximo de registros por llamada a la API de Zoho


def now():
    return datetime.now(ZoneInfo("America/Santiago")).isoformat(timespec="seconds")


def read_rows(path, sheet=None):
    p = Path(path)
    if p.suffix.lower() in (".xlsx", ".xlsm"):
        import openpyxl
        wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
        ws = wb[sheet] if sheet else wb.worksheets[0]
        it = ws.iter_rows(values_only=True)
        header = [str(h).strip() if h is not None else "" for h in next(it)]
        return [dict(zip(header, r)) for r in it if any(v not in (None, "") for v in r)]
    if p.suffix.lower() == ".json":
        return json.loads(p.read_text())
    raw = p.read_bytes()
    text = raw.decode("utf-8-sig") if raw[:3] == b"\xef\xbb\xbf" else raw.decode("utf-8", errors="strict") \
        if _is_utf8(raw) else raw.decode("latin-1")
    dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t|")
    return [r for r in csv.DictReader(text.splitlines(), dialect=dialect) if any((v or "").strip() for v in r.values())]


def _is_utf8(raw):
    try:
        raw.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def row_key(module, record):
    blob = json.dumps({"m": module, "r": record}, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def resolve_owner(value, users):
    key = n.name_key(value)
    hits = [u for u in users if u["status"] == "active" and key and (
        key == n.name_key(u["full_name"]) or key in n.name_key(u["full_name"]))]
    return ({"id": hits[0]["id"]}, None) if len(hits) == 1 else (None, f"propietario no resuelto o ambiguo: {value!r}")


def plan(module, input_path, source, out_dir, overrides=None, defaults=None, sheet=None, schema_dir=SCHEMA_DIR):
    """Lee el origen, mapea, normaliza y valida. No consulta ni escribe en Zoho."""
    schema = Schema(module, schema_dir)
    users = json.loads((Path(schema_dir) / "users.json").read_text())
    rows = read_rows(input_path, sheet)
    cols = list(rows[0].keys()) if rows else []
    colmap, unmapped = mapping.build_column_map(cols, schema, overrides)
    out = []
    for i, raw in enumerate(rows, start=2 if Path(input_path).suffix.lower() != ".json" else 1):
        rec, prov, issues = {}, {}, []
        for col, api in colmap.items():
            val = raw.get(col)
            if val in (None, ""):
                continue
            if api == "Owner":
                v, err = resolve_owner(val, users)
            elif schema.fields[api]["data_type"] == "lookup":
                v, err = {"_name": n.clean(val)}, None  # se resuelve a id en classify
            else:
                v, err = mapping.normalize_value(api, val, schema)
            if err:
                issues.append(f"{col}: {err}")
            if v not in (None, ""):
                if api in rec and rec[api] != v:
                    if api == "Last_Name" and "First_Name" not in rec:
                        rec[api] = f"{rec[api]} {v}"
                        continue
                    issues.append(f"columnas en conflicto para {api}")
                rec[api] = v
                prov[api] = "confirmado"
        for api, v in (defaults or {}).items():
            if rec.get(api) in (None, ""):
                rec[api] = v
                prov[api] = "instrucción"
        val_rec = {k: v for k, v in rec.items() if not (isinstance(v, dict) and "_name" in v)}
        issues += [x for x in schema.validate(val_rec, for_create=True)
                   if not any(f"{k} " in x or x.endswith(k) for k, v in rec.items() if isinstance(v, dict))]
        rec.update(val_rec)
        out.append({"row_key": row_key(module, rec), "source_row": i, "record": rec, "provenance": prov,
                    "unknown": [a for a in schema.mandatory() if a not in rec],
                    "issues": issues, "lookups": dedup.lookup_queries(module, rec)})
    run = Path(out_dir)
    run.mkdir(parents=True, exist_ok=True)
    meta = {"module": module, "source": source, "input": str(input_path), "created": now(),
            "column_map": colmap, "unmapped_columns": unmapped, "defaults": defaults or {},
            "layout_id": schema.default_layout_id, "rows": len(out)}
    (run / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    (run / "rows.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    return meta, out


def classify(run_dir, candidates_path):
    """candidates.json: {row_key: [registros Zoho con _module]}, y opcional "_accounts": {nombre: id}."""
    run = Path(run_dir)
    meta = json.loads((run / "meta.json").read_text())
    rows = json.loads((run / "rows.json").read_text())
    cands = json.loads(Path(candidates_path).read_text())
    accounts = {n.company_key(k): v for k, v in (cands.get("_accounts") or {}).items()}
    done = completed_keys(run)
    module = meta["module"]
    plan_rows = []
    for r in rows:
        rec = dict(r["record"])
        issues = list(r["issues"])
        for k, v in list(rec.items()):
            if isinstance(v, dict) and "_name" in v:
                acc_id = accounts.get(n.company_key(v["_name"]))
                if acc_id:
                    rec[k] = {"id": acc_id}
                else:
                    issues.append(f"{k}: cuenta '{v['_name']}' no encontrada en el CRM")
                    rec.pop(k)
        res = dedup.classify(module, rec, cands.get(r["row_key"], []))
        entry = {"row_key": r["row_key"], "source_row": r["source_row"], "dedup": res, "issues": issues,
                 "provenance": r["provenance"]}
        if r["row_key"] in done:
            entry.update(action="omitir", why="ya procesado en ejecución anterior")
        elif res["status"] == dedup.EXISTING:
            existing = next(c for c in cands[r["row_key"]] if c["id"] == res["match_id"])
            upd, conflicts = dedup.merge_update(rec, existing)
            entry.update(action="actualizar" if upd else "omitir", record_id=res["match_id"],
                         payload=dict(upd, id=res["match_id"]) if upd else None, conflicts=conflicts,
                         why=None if upd else "sin campos nuevos que completar")
        elif res["status"] == dedup.NEW and not [i for i in issues if i.startswith("falta obligatorio")
                                                    or "no permitido" in i or "no encontrada" in i]:
            entry.update(action="crear", payload=dict(rec, Layout={"id": meta["layout_id"]}))
        elif res["status"] == dedup.NEW:
            entry.update(action="error", why="datos obligatorios o inválidos")
        else:
            entry.update(action="revisar", why=res["status"])
        plan_rows.append(entry)
    creates = [p for p in plan_rows if p["action"] == "crear"]
    updates = [p for p in plan_rows if p["action"] == "actualizar"]
    chunks = []
    for kind, items in (("crear", creates), ("actualizar", updates)):
        for i in range(0, len(items), CHUNK):
            part = items[i:i + CHUNK]
            chunks.append({"chunk": len(chunks) + 1, "action": kind, "row_keys": [p["row_key"] for p in part],
                           "body": {"data": [p["payload"] for p in part]}})
    planned = {"module": module, "created": now(), "rows": plan_rows, "chunks": chunks}
    (run / "plan.json").write_text(json.dumps(planned, ensure_ascii=False, indent=1, default=str))
    (run / "preview.md").write_text(preview(meta, planned))
    return planned


def preview(meta, planned):
    rows = planned["rows"]
    count = {}
    for r in rows:
        count[r["action"]] = count.get(r["action"], 0) + 1
    L = [f"# Previsualización de carga — {meta['module']}", "",
         f"- Fuente: {meta['source']}", f"- Archivo: `{Path(meta['input']).name}`", f"- Generado: {planned['created']}",
         f"- Filas: {len(rows)} → " + ", ".join(f"**{k}**: {v}" for k, v in sorted(count.items())),
         f"- Columnas sin mapear (se ignoran): {', '.join(meta['unmapped_columns']) or 'ninguna'}",
         f"- Valores por instrucción: {meta['defaults'] or 'ninguno'}", "",
         "| Fila | Acción | Dedup | Detalle |", "|---|---|---|---|"]
    for r in rows:
        cids = r["dedup"]["candidate_ids"]
        det = "; ".join(filter(None, [r.get("why"), "; ".join(dict.fromkeys(r["dedup"]["reasons"])),
                                      ("candidatos: " + ", ".join(cids)) if cids else None,
                                      "; ".join(r["issues"]),
                                      "conflictos: " + ", ".join(c["field"] for c in r.get("conflicts", []))
                                      if r.get("conflicts") else None]))
        L.append(f"| {r['source_row']} | {r['action']} | {r['dedup']['status']} | {det.replace('|', '/')} |")
    L += ["", "## Muestra de payloads (datos sensibles enmascarados)", ""]
    for r in [x for x in rows if x.get("payload")][:5]:
        L.append("```json\n" + json.dumps({k: mask(k, v) for k, v in r["payload"].items()},
                                          ensure_ascii=False, indent=1, default=str) + "\n```")
    return "\n".join(L) + "\n"


def completed_keys(run):
    log = Path(run) / "audit.jsonl"
    if not log.exists():
        return set()
    return {e["row_key"] for e in map(json.loads, log.read_text().splitlines())
            if e.get("result") in ("creado", "actualizado")}


def record(run_dir, chunk_no, response_path):
    """Registra la respuesta de Zoho de un chunk ejecutado. Hace la ejecución reanudable e idempotente."""
    run = Path(run_dir)
    meta = json.loads((run / "meta.json").read_text())
    planned = json.loads((run / "plan.json").read_text())
    chunk = next(c for c in planned["chunks"] if c["chunk"] == chunk_no)
    resp = json.loads(Path(response_path).read_text())
    items = resp.get("data", {}).get("data") if isinstance(resp.get("data"), dict) else resp.get("data")
    by_key = {r["row_key"]: r for r in planned["rows"]}
    written = json.loads((run / "written.json").read_text()) if (run / "written.json").exists() else {}
    with (run / "audit.jsonl").open("a") as log:
        for key, body, item in zip(chunk["row_keys"], chunk["body"]["data"], items or []):
            ok = item.get("status") == "success"
            rid = (item.get("details") or {}).get("id")
            entry = {"timestamp": now(), "source": meta["source"], "module": meta["module"], "row_key": key,
                     "source_row": by_key[key]["source_row"], "record_id": rid,
                     "result": ("creado" if chunk["action"] == "crear" else "actualizado") if ok else "error",
                     "fields": sorted(k for k in body if k not in ("id", "Layout")),
                     "values": {k: mask(k, v) for k, v in body.items() if k != "Layout"},
                     "conflicts": [{"field": c["field"], "crm": mask(c["field"], c["crm"]),
                                    "source": mask(c["field"], c["source"])} for c in by_key[key].get("conflicts", [])],
                     "zoho": {"code": item.get("code"), "message": item.get("message")}}
            log.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
            if ok:
                written[key] = {"record_id": rid, "payload": body}
    # Copia local sin enmascarar para la conciliación posterior (runs/ no se versiona).
    (run / "written.json").write_text(json.dumps(written, ensure_ascii=False, indent=1, default=str))
    return completed_keys(run)


def report(run_dir):
    run = Path(run_dir)
    meta = json.loads((run / "meta.json").read_text())
    planned = json.loads((run / "plan.json").read_text())
    log = [json.loads(l) for l in (run / "audit.jsonl").read_text().splitlines()] if (run / "audit.jsonl").exists() else []
    last = {e["row_key"]: e for e in log}
    L = [f"# Reporte de auditoría — {meta['module']}", "", f"- Fuente: {meta['source']}",
         f"- Generado: {now()}", "", "| Fila | Acción | ID Zoho | Resultado | Campos | Respuesta Zoho |",
         "|---|---|---|---|---|---|"]
    for r in planned["rows"]:
        e = last.get(r["row_key"])
        res = e["result"] if e else ("omitido" if r["action"] in ("omitir",) else
                                     "pendiente" if r["action"] in ("crear", "actualizar") else r["action"])
        L.append(f"| {r['source_row']} | {r['action']} | {(e or {}).get('record_id') or r.get('record_id') or ''} | "
                 f"{res} | {', '.join((e or {}).get('fields', []))} | {((e or {}).get('zoho') or {}).get('code', '')} |")
    text = "\n".join(L) + "\n"
    (run / "report.md").write_text(text)
    return text


def verify(run_dir, fetched_path):
    """Compara registros releídos desde Zoho ({id: registro}) con lo escrito. Devuelve diferencias."""
    run = Path(run_dir)
    fetched = json.loads(Path(fetched_path).read_text())
    written = json.loads((run / "written.json").read_text())
    diffs = []
    for w in written.values():
        got = fetched.get(w["record_id"])
        if got is None:
            diffs.append({"record_id": w["record_id"], "field": "*", "expected": "registro", "got": "no releído"})
            continue
        for k, v in w["payload"].items():
            if k in ("id", "Layout"):
                continue
            g = got.get(k)
            if isinstance(v, dict):
                same = (g or {}).get("id") == v.get("id")
            elif isinstance(v, list):
                same = sorted(map(str, v)) == sorted(map(str, g or []))
            else:
                same = str(g).strip().lower() == str(v).strip().lower() or \
                    (k in ("Phone", "Mobile") and n.phone_cl(g)[0] == v)
            if not same:
                diffs.append({"record_id": w["record_id"], "field": k, "expected": mask(k, v), "got": mask(k, g)})
    return diffs
