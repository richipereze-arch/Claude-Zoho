"""Validación de registros contra el esquema real exportado en schema/<Module>.fields.json."""
import json
from pathlib import Path

from . import normalize as n

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schema"

# Campos tratados como dato personal restringido: se enmascaran en reportes y logs.
SENSITIVE = {"RUT", "Date_of_Birth"}


class Schema:
    def __init__(self, module, schema_dir=SCHEMA_DIR):
        data = json.loads((Path(schema_dir) / f"{module}.fields.json").read_text())
        self.module = module
        self.layouts = data["layouts"]
        self.fields = {f["api_name"]: f for f in data["fields"]}

    @property
    def default_layout_id(self):
        active = [l for l in self.layouts if l.get("status") == "active"]
        return active[0]["id"] if active else None

    def mandatory(self):
        return [a for a, f in self.fields.items() if f["system_mandatory"] or f["layout_mandatory"]]

    def picklist_match(self, api_name, value):
        """Devuelve el valor de display exacto aceptado por el CRM o None si no existe la opción."""
        opts = self.fields[api_name].get("picklist_values") or []
        if not opts:
            return value
        key = n.name_key(value)
        for o in opts:
            if key in (n.name_key(o["display"]), n.name_key(o["actual"])):
                return o["display"]
        return None

    def validate(self, record, for_create=True):
        """Valida un registro {api_name: valor}. Devuelve lista de problemas (vacía si es válido)."""
        issues = []
        for api, value in record.items():
            f = self.fields.get(api)
            if f is None:
                issues.append(f"campo inexistente en {self.module}: {api}")
                continue
            if not f["api_writable"] or f["formula"]:
                issues.append(f"campo no escribible vía API: {api}")
                continue
            dt = f["data_type"]
            if dt in ("picklist",) and value is not None:
                ok = self.picklist_match(api, value)
                if ok is None:
                    issues.append(f"valor no permitido en {api}: {value!r}")
                else:
                    record[api] = ok
            elif dt == "multiselectpicklist" and value is not None:
                vals = value if isinstance(value, list) else [v.strip() for v in str(value).split(";")]
                out = []
                for v in vals:
                    ok = self.picklist_match(api, v)
                    if ok is None:
                        issues.append(f"valor no permitido en {api}: {v!r}")
                    else:
                        out.append(ok)
                record[api] = out
            elif dt in ("text", "email", "phone", "website", "textarea") and value is not None:
                if f.get("length") and len(str(value)) > int(f["length"]):
                    issues.append(f"{api} excede largo máximo {f['length']}")
        if for_create:
            for api in self.mandatory():
                if record.get(api) in (None, "", []):
                    kind = "sistema" if self.fields[api]["system_mandatory"] else "layout"
                    issues.append(f"falta obligatorio ({kind}): {api} ({self.fields[api]['label']})")
        return issues


def mask(api_name, value):
    if value in (None, ""):
        return value
    s = str(value)
    if api_name in SENSITIVE:
        return "***" + s[-3:]
    if "@" in s:
        user, _, dom = s.partition("@")
        return user[:2] + "***@" + dom
    if api_name in ("Phone", "Mobile", "Other_Phone", "Home_Phone", "Asst_Phone"):
        return s[:4] + "****" + s[-2:]
    return value
