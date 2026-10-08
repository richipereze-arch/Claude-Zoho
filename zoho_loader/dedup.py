"""Clasificación de duplicados: nuevo, existente, posible_duplicado o ambiguo.

Las búsquedas en Zoho las hace Claude vía MCP (searchRecords / COQL) usando las consultas de
`lookup_queries`; los candidatos devueltos se pasan a `classify`.
Regla de oro: solo una coincidencia fuerte y única convierte una fila en "existente".
"""
from difflib import SequenceMatcher

from . import normalize as n

NEW, EXISTING, POSSIBLE, AMBIGUOUS = "nuevo", "existente", "posible_duplicado", "ambiguo"


def lookup_queries(module, rec):
    """Consultas de búsqueda a ejecutar en Zoho para una fila normalizada."""
    q = []
    if module in ("Leads", "Contacts"):
        if rec.get("Email"):
            q += [{"module": "Leads", "email": rec["Email"]}, {"module": "Contacts", "email": rec["Email"]}]
        for ph in {rec.get("Phone"), rec.get("Mobile")} - {None}:
            q += [{"module": "Leads", "phone": ph[-9:]}, {"module": "Contacts", "phone": ph[-9:]}]
        if rec.get("Last_Name") and not q:
            q.append({"module": module, "word": rec["Last_Name"]})
    elif module == "Accounts":
        if rec.get("RUT"):
            q.append({"module": "Accounts", "criteria": f"(RUT:equals:{rec['RUT']})"})
        if rec.get("Account_Name"):
            q.append({"module": "Accounts", "word": n.company_key(rec["Account_Name"]) or rec["Account_Name"]})
    elif module == "Deals":
        if rec.get("Deal_Name"):
            q.append({"module": "Deals", "word": rec["Deal_Name"]})
    return q


def _sim(a, b):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def _phones(c):
    return {p[-9:] for p in (n.phone_cl(c.get(k))[0] for k in ("Phone", "Mobile")) if p}


def classify(module, rec, candidates):
    """candidates: registros devueltos por Zoho (dicts con id, Email, Phone, Mobile, Last_Name, Account_Name, RUT...).
    Devuelve dict(status, match_id, reasons, candidates)."""
    seen, cands = set(), []
    for c in candidates:
        if c.get("id") not in seen:
            seen.add(c.get("id"))
            cands.append(c)
    strong, weak = [], []
    if module in ("Leads", "Contacts"):
        email = rec.get("Email")
        phones = {p[-9:] for p in (rec.get("Phone"), rec.get("Mobile")) if p}
        name = n.name_key(" ".join(filter(None, [rec.get("First_Name"), rec.get("Last_Name")])))
        for c in cands:
            cmod = c.get("_module", module)
            cname = n.name_key(c.get("Full_Name") or " ".join(filter(None, [c.get("First_Name"), c.get("Last_Name")])))
            same_email = bool(email) and (n.email(c.get("Email"))[0] == email)
            same_phone = bool(phones & _phones(c))
            name_sim = _sim(name, cname)
            if cmod != module and (same_email or same_phone):
                weak.append((c, f"ya existe en {cmod} (email/teléfono)"))
            elif same_email:
                strong.append((c, "mismo correo"))
            elif same_phone and name_sim >= 0.85:
                strong.append((c, f"mismo teléfono y nombre similar ({name_sim:.2f})"))
            elif same_phone:
                weak.append((c, "mismo teléfono, nombre distinto"))
            elif name_sim >= 0.92:
                weak.append((c, f"nombre muy similar ({name_sim:.2f})"))
    elif module == "Accounts":
        ck = n.company_key(rec.get("Account_Name"))
        for c in cands:
            if rec.get("RUT") and c.get("RUT") and n.rut(c["RUT"])[0] == rec["RUT"]:
                strong.append((c, "mismo RUT"))
                continue
            sim = _sim(ck, n.company_key(c.get("Account_Name")))
            if sim == 1.0:
                strong.append((c, "misma razón social normalizada"))
            elif sim >= 0.88:
                weak.append((c, f"razón social similar ({sim:.2f})"))
    elif module == "Deals":
        dk = n.name_key(rec.get("Deal_Name"))
        acc = (rec.get("Account_Name") or {}).get("id") if isinstance(rec.get("Account_Name"), dict) else None
        for c in cands:
            same_name = n.name_key(c.get("Deal_Name")) == dk
            c_acc = (c.get("Account_Name") or {}).get("id") if isinstance(c.get("Account_Name"), dict) else None
            if same_name and acc and c_acc == acc:
                strong.append((c, "mismo nombre de trato y cuenta"))
            elif same_name:
                weak.append((c, "mismo nombre de trato, cuenta distinta o desconocida"))
    ids = {c["id"] for c, _ in strong}
    if len(ids) == 1 and not [w for w in weak if w[0]["id"] not in ids and "ya existe en" not in w[1]]:
        c, why = strong[0]
        extra = [w[1] for w in weak]
        return {"status": EXISTING, "match_id": c["id"], "reasons": [why] + extra, "candidate_ids": sorted(ids)}
    if len(ids) > 1:
        return {"status": AMBIGUOUS, "match_id": None, "reasons": ["varias coincidencias fuertes"],
                "candidate_ids": sorted(ids)}
    if strong or weak:
        allc = sorted({c["id"] for c, _ in strong + weak})
        return {"status": POSSIBLE if not strong else AMBIGUOUS, "match_id": None,
                "reasons": [w for _, w in strong + weak], "candidate_ids": allc}
    return {"status": NEW, "match_id": None, "reasons": [], "candidate_ids": []}


def merge_update(rec, existing, protected=("Owner",)):
    """Prepara actualización conservadora: solo completa campos vacíos en el CRM.
    Devuelve (payload_update, conflictos). Nunca sobrescribe valores distintos."""
    upd, conflicts = {}, []
    for k, v in rec.items():
        if v in (None, "", []) or k in protected:
            continue
        cur = existing.get(k)
        if cur in (None, "", [], "-", "-None-"):
            upd[k] = v
        elif isinstance(cur, dict) or isinstance(v, dict):
            if (cur or {}).get("id") != (v or {}).get("id"):
                conflicts.append({"field": k, "crm": cur, "source": v})
        elif str(cur).strip().lower() != str(v).strip().lower():
            if k in ("Phone", "Mobile") and n.phone_cl(cur)[0] == v:
                continue
            conflicts.append({"field": k, "crm": cur, "source": v})
    return upd, conflicts
