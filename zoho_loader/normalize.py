"""Normalizadores. Cada función devuelve (valor_normalizado, problema) — problema es None si todo va bien.

Nunca inventan datos: si el valor no se puede interpretar con certeza, devuelven (None, motivo).
"""
import re
import unicodedata
from datetime import datetime, date

EMAIL_RE = re.compile(r"^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$")


def clean(value):
    if value is None:
        return None
    s = str(value).strip()
    s = re.sub(r"\s+", " ", s)
    return s or None


def email(value):
    s = clean(value)
    if s is None:
        return None, None
    s = s.lower().replace("mailto:", "").strip(" <>;,")
    if not EMAIL_RE.match(s):
        return None, f"correo inválido: {value!r}"
    return s, None


def phone_cl(value):
    """Normaliza teléfonos chilenos a E.164 (+56XXXXXXXXX). Números extranjeros con '+' se conservan."""
    s = clean(value)
    if s is None:
        return None, None
    raw = s
    intl = s.startswith("+") or s.startswith("00")
    digits = re.sub(r"\D", "", s)
    if s.startswith("00"):
        digits = digits[2:]
    if intl and not digits.startswith("56"):
        if 8 <= len(digits) <= 15:
            return "+" + digits, None
        return None, f"teléfono internacional inválido: {raw!r}"
    if digits.startswith("56"):
        digits = digits[2:]
    digits = digits.lstrip("0")
    if len(digits) == 8 and digits[0] in "2345679":
        # Número antiguo sin el 9 de móviles o sin código de área: ambiguo, no se completa.
        return None, f"teléfono de 8 dígitos ambiguo (falta prefijo): {raw!r}"
    if len(digits) == 9:
        return "+56" + digits, None
    return None, f"teléfono no reconocido: {raw!r}"


def rut(value):
    """Valida y formatea RUT/RUN chileno (12.345.678-5). Dato personal restringido: solo si existe uso legítimo."""
    s = clean(value)
    if s is None:
        return None, None
    s = s.upper().replace(".", "").replace(" ", "")
    m = re.match(r"^(\d{1,8})-?([\dK])$", s)
    if not m:
        return None, "RUT con formato inválido"
    body, dv = m.groups()
    total, mult = 0, 2
    for d in reversed(body):
        total += int(d) * mult
        mult = 2 if mult == 7 else mult + 1
    expected = 11 - total % 11
    expected = "0" if expected == 11 else "K" if expected == 10 else str(expected)
    if dv != expected:
        return None, "RUT con dígito verificador incorrecto"
    return f"{int(body):,}".replace(",", ".") + "-" + dv, None


def person_name(value):
    s = clean(value)
    if s is None:
        return None, None
    if s.isupper() or s.islower():
        small = {"de", "del", "la", "las", "los", "y", "da", "van", "von"}
        s = " ".join(w if (i and w.lower() in small) else w.capitalize() for i, w in enumerate(s.lower().split(" ")))
        s = s[0].upper() + s[1:]
    return s, None


LEGAL_SUFFIXES = [r"s\.?p\.?a\.?", r"s\.?a\.?", r"ltda\.?", r"limitada", r"e\.?i\.?r\.?l\.?",
                  r"spa", r"s\.?a\.?c\.?", r"y\s+c[ií]a\.?", r"compa[ñn][ií]a", r"inc\.?", r"llc"]


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def company_key(value):
    """Clave de comparación para razones sociales: sin tildes, sin sufijos societarios, sin puntuación."""
    s = clean(value)
    if s is None:
        return None
    s = strip_accents(s.lower())
    for suf in LEGAL_SUFFIXES:
        s = re.sub(rf"(\s|,)+{suf}\s*$", "", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip() or None


def name_key(value):
    s = clean(value)
    return re.sub(r"[^a-z0-9 ]", "", strip_accents(s.lower())) if s else None


DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d/%m/%y", "%d-%m-%y", "%Y/%m/%d"]


def date_iso(value):
    """Fechas a ISO (YYYY-MM-DD). Se asume orden día/mes (Chile); nunca mes/día."""
    if value is None or value == "":
        return None, None
    if isinstance(value, datetime):
        return value.date().isoformat(), None
    if isinstance(value, date):
        return value.isoformat(), None
    s = clean(value)
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s.split(" ")[0].split("T")[0], fmt).date().isoformat(), None
        except ValueError:
            continue
    return None, f"fecha no reconocida: {value!r}"


def amount(value):
    """Montos: acepta '$1.234.567', '1.234.567,50', 'USD 1,500.25', 1500. Devuelve (float, problema)."""
    if value is None or value == "":
        return None, None
    if isinstance(value, (int, float)):
        return float(value), None
    s = clean(value)
    s = re.sub(r"(?i)(clp|usd|us\$|ch\$|\$|uf)", "", s).replace(" ", "")
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", s) or re.fullmatch(r"-?\d+,\d{1,2}", s):
        s = s.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", s):
        s = s.replace(",", "")
    try:
        return float(s), None
    except ValueError:
        return None, f"monto no reconocido: {value!r}"


def currency(value):
    s = (clean(value) or "").upper()
    if not s:
        return None, None
    if s in {"CLP", "$", "CH$", "PESOS", "PESO"}:
        return "CLP", None
    if s in {"USD", "US$", "DOLAR", "DÓLAR", "DOLARES", "DÓLARES"}:
        return "USD", None
    return None, f"moneda no habilitada en el CRM (solo CLP/USD): {value!r}"


def website(value):
    s = clean(value)
    if s is None:
        return None, None
    if not re.match(r"^https?://", s, re.I):
        s = "https://" + s
    return s, None
