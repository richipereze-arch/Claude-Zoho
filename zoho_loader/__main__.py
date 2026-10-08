import argparse
import json
import sys

from . import pipeline


def kv(items):
    out = {}
    for it in items or []:
        k, _, v = it.partition("=")
        out[k] = v
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python3 -m zoho_loader")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="mapear, normalizar y validar un archivo (sin tocar Zoho)")
    p.add_argument("--module", required=True)
    p.add_argument("--input", required=True)
    p.add_argument("--source", required=True, help="descripción de la fuente para auditoría")
    p.add_argument("--run", required=True, help="carpeta del lote, p.ej. runs/2026-10-08-leads-feria")
    p.add_argument("--sheet")
    p.add_argument("--map", nargs="*", help="columna=API_name para forzar el mapeo")
    p.add_argument("--set", nargs="*", help="API_name=valor a aplicar cuando falte (por instrucción)")
    c = sub.add_parser("classify", help="clasificar duplicados con candidatos obtenidos vía MCP")
    c.add_argument("--run", required=True)
    c.add_argument("--candidates", required=True)
    r = sub.add_parser("record", help="registrar la respuesta de Zoho de un chunk ejecutado")
    r.add_argument("--run", required=True)
    r.add_argument("--chunk", type=int, required=True)
    r.add_argument("--response", required=True)
    rep = sub.add_parser("report", help="reporte de auditoría del lote")
    rep.add_argument("--run", required=True)
    v = sub.add_parser("verify", help="conciliación posterior contra registros releídos")
    v.add_argument("--run", required=True)
    v.add_argument("--fetched", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "plan":
        meta, rows = pipeline.plan(a.module, a.input, a.source, a.run, kv(a.map), kv(a.set), a.sheet)
        bad = sum(1 for r in rows if r["issues"])
        print(json.dumps({"rows": len(rows), "rows_with_issues": bad, "unmapped": meta["unmapped_columns"],
                          "column_map": meta["column_map"], "lookups_needed": sum(len(r["lookups"]) for r in rows)},
                         ensure_ascii=False, indent=1))
    elif a.cmd == "classify":
        planned = pipeline.classify(a.run, a.candidates)
        print(open(f"{a.run}/preview.md").read())
    elif a.cmd == "record":
        print(f"filas completadas: {len(pipeline.record(a.run, a.chunk, a.response))}")
    elif a.cmd == "report":
        print(pipeline.report(a.run))
    elif a.cmd == "verify":
        diffs = pipeline.verify(a.run, a.fetched)
        print(json.dumps(diffs, ensure_ascii=False, indent=1) if diffs else "OK: los datos escritos coinciden")
        sys.exit(1 if diffs else 0)


if __name__ == "__main__":
    main()
