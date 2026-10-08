"""Build the Zoho CRM data dictionary from raw getFields / getLayouts metadata.

Usage: python3 tools/build_dictionary.py <meta_dir> <out_dir>
  meta_dir contains <Module>.json (getFields output) and L_<Module>.json (getLayouts output).
Outputs schema/<Module>.fields.json (compact, machine-readable) and docs/02_diccionario_de_datos.md.
Only metadata is processed; no record data or credentials are read or written.
"""
import json
import sys
from pathlib import Path

MODULES = ["Leads", "Contacts", "Accounts", "Deals", "Tasks"]
SYSTEM_READONLY = {"Created_By", "Modified_By", "Created_Time", "Modified_Time", "id",
                   "Last_Activity_Time", "Locked__s", "Record_Status__s", "Exchange_Rate",
                   "Tag", "Closed_Time"}


def load(path):
    return json.loads(Path(path).read_text())


def layout_info(meta_dir, module):
    p = Path(meta_dir) / f"L_{module}.json"
    if not p.exists():
        return {}, []
    layouts = load(p)["data"]["layouts"]
    info = {}
    for lay in layouts:
        for sec in lay.get("sections", []):
            for f in sec.get("fields", []) or []:
                e = info.setdefault(f["api_name"], {"required": False, "validation": False, "sections": set()})
                e["required"] |= bool(f.get("required"))
                e["validation"] |= bool(f.get("validation_rule"))
                e["sections"].add(sec.get("display_label"))
    return info, [{"name": l["name"], "id": l["id"], "status": l.get("status")} for l in layouts]


def compact(f, lay):
    picks = [p.get("actual_value") if p.get("actual_value") == p.get("display_value")
             else f'{p.get("display_value")} [{p.get("actual_value")}]'
             for p in f.get("pick_list_values") or [] if p.get("display_value") != "-None-"]
    lk = f.get("lookup") or {}
    op = f.get("operation_type") or {}
    return {
        "api_name": f["api_name"],
        "label": f.get("field_label"),
        "data_type": f.get("data_type"),
        "custom": f.get("custom_field", False),
        "system_mandatory": f.get("system_mandatory", False),
        "layout_mandatory": bool(lay.get("required")),
        "unique": bool(f.get("unique")),
        "api_writable": bool(op.get("api_create") or op.get("api_update")),
        "read_only": bool(f.get("read_only") or f.get("field_read_only")),
        "length": f.get("length"),
        "lookup_module": (lk.get("module") or {}).get("api_name"),
        "picklist": picks,
        "picklist_values": [{"display": p.get("display_value"), "actual": p.get("actual_value")}
                            for p in f.get("pick_list_values") or [] if p.get("display_value") != "-None-"],
        "encrypted": bool(f.get("crypt")),
        "formula": bool(f.get("formula")),
        "has_validation_rule": bool(lay.get("validation")),
        "tooltip": (f.get("tooltip") or {}).get("value"),
        "in_layout": bool(lay),
    }


def obs(c):
    o = []
    if c["system_mandatory"]:
        o.append("Obligatorio de sistema")
    elif c["layout_mandatory"]:
        o.append("Obligatorio por layout")
    if c["unique"]:
        o.append("Único")
    if c["custom"]:
        o.append("Personalizado")
    if c["lookup_module"]:
        o.append(f"Lookup → {c['lookup_module']}")
    if c["formula"]:
        o.append("Fórmula")
    if c["encrypted"]:
        o.append("Cifrado")
    if not c["api_writable"]:
        o.append("No escribible vía API")
    if c["tooltip"]:
        o.append(f"Tooltip: {c['tooltip']}")
    return "; ".join(o)


def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def main(meta_dir, out_dir):
    out = Path(out_dir)
    lines = ["# 02 · Diccionario de datos — Zoho CRM (Banca Inversiones)", "",
             "Generado automáticamente por `tools/build_dictionary.py` desde la metadata real "
             "(`getFields` + `getLayouts`) vía el conector MCP oficial. Solo metadata: no contiene registros.", "",
             "Leyenda *Oblig.*: **S** = obligatorio de sistema, **L** = obligatorio por layout, vacío = opcional.", ""]
    for m in MODULES:
        fp = Path(meta_dir) / f"{m}.json"
        if not fp.exists():
            continue
        fields = load(fp)["data"]["fields"]
        lay, layouts = layout_info(meta_dir, m)
        comp = [compact(f, lay.get(f["api_name"], {})) for f in fields]
        (out / "schema").mkdir(parents=True, exist_ok=True)
        (out / "schema" / f"{m}.fields.json").write_text(
            json.dumps({"module": m, "layouts": layouts, "fields": comp}, ensure_ascii=False, indent=1))
        lines += [f"## {m}", ""]
        if layouts:
            lines.append("Layouts: " + ", ".join(f"{l['name']} (`{l['id']}`, {l['status']})" for l in layouts))
            lines.append("")
        lines += ["| Campo visible | API name | Tipo | Oblig. | Valores permitidos | Observaciones |",
                  "|---|---|---|---|---|---|"]
        for c in sorted(comp, key=lambda c: (not (c["system_mandatory"] or c["layout_mandatory"]), not c["custom"], c["label"] or "")):
            if c["api_name"] in SYSTEM_READONLY:
                continue
            ob = "S" if c["system_mandatory"] else ("L" if c["layout_mandatory"] else "")
            vals = "; ".join(c["picklist"])
            lines.append(f"| {md_escape(c['label'])} | `{c['api_name']}` | {c['data_type']} | {ob} | "
                         f"{md_escape(vals)} | {md_escape(obs(c))} |")
        lines.append("")
    lines += ["Campos de sistema omitidos de las tablas (solo lectura): " + ", ".join(f"`{s}`" for s in sorted(SYSTEM_READONLY)), ""]
    (out / "docs" / "02_diccionario_de_datos.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
