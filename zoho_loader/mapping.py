"""Mapeo de columnas de origen (Excel/CSV/texto) a API names reales del CRM."""
import re

from . import normalize as n

# Alias curados por módulo (clave normalizada → API name). Se complementan con etiquetas y API names del esquema.
ALIASES = {
    "common": {
        "correo": "Email", "email": "Email", "mail": "Email", "e mail": "Email", "correo electronico": "Email",
        "telefono": "Phone", "fono": "Phone", "phone": "Phone",
        "celular": "Mobile", "movil": "Mobile", "whatsapp": "Mobile", "cel": "Mobile",
        "nombre": "First_Name", "nombres": "First_Name",
        "apellido": "Last_Name", "apellidos": "Last_Name",
        "nombre completo": "Last_Name",
        "rut": "RUT", "run": "RUT",
        "descripcion": "Description", "observaciones": "Description", "comentarios": "Description",
        "producto": "Producto", "ejecutivo": "Ejecutivo_Junior", "ejecutivo junior": "Ejecutivo_Junior",
        "analista": "Analista_de_Inversiones", "fuente": "Lead_Source", "origen": "Lead_Source",
        "cargo": "Title", "sitio web": "Website", "web": "Website",
        "comuna": "Comuna_Ciudad", "ciudad": "City", "region": "State", "direccion": "Street",
        "propietario": "Owner", "responsable": "Owner",
    },
    "Leads": {"empresa": "Company", "compania": "Company", "razon social": "Company", "nombre cuenta": "Company",
              "estado": "Lead_Status", "atributo": "Atributo_del_Prospecto", "broker": "Broker_FK",
              "fase": "Fase_FinanciaK"},
    "Contacts": {"empresa": "Account_Name", "cuenta": "Account_Name", "razon social": "Account_Name"},
    "Accounts": {"empresa": "Account_Name", "razon social": "Account_Name", "nombre": "Account_Name",
                 "cuenta": "Account_Name", "etapa": "IBs_Atributo", "modalidad": "Account_Type",
                 "calificacion": "Rating", "telefono": "Phone", "celular": "Phone", "movil": "Phone",
                 "correo": "Correo_Contacto", "email": "Correo_Contacto"},
    "Deals": {"trato": "Deal_Name", "negocio": "Deal_Name", "oportunidad": "Deal_Name",
              "cuenta": "Account_Name", "empresa": "Account_Name", "contacto": "Contact_Name",
              "monto": "Amount", "importe": "Amount", "etapa": "Stage", "fase": "Stage",
              "fecha cierre": "Closing_Date", "fecha de cierre": "Closing_Date", "tipo": "Type"},
}

# Normalizador por tipo de dato del CRM.
BY_TYPE = {"email": n.email, "phone": n.phone_cl, "date": n.date_iso, "currency": n.amount,
           "double": n.amount, "website": n.website}
BY_FIELD = {"RUT": n.rut, "First_Name": n.person_name, "Last_Name": n.person_name, "Currency": n.currency}


def key(col):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", n.strip_accents(str(col).lower()))).strip()


def build_column_map(columns, schema, overrides=None):
    """Devuelve ({columna: api_name}, [columnas sin mapear]). overrides: {columna: api_name} explícitos."""
    overrides = overrides or {}
    lookup = {}
    for api, f in schema.fields.items():
        lookup[key(api.replace("_", " "))] = api
        if f.get("label"):
            lookup[key(f["label"])] = api
    lookup.update(ALIASES["common"])
    lookup.update(ALIASES.get(schema.module, {}))
    mapping, unmapped = {}, []
    for col in columns:
        if col in overrides:
            mapping[col] = overrides[col]
            continue
        api = lookup.get(key(col))
        if api and api in schema.fields:
            mapping[col] = api
        else:
            unmapped.append(col)
    return mapping, unmapped


def normalize_value(api, value, schema):
    f = schema.fields.get(api, {})
    fn = BY_FIELD.get(api) or BY_TYPE.get(f.get("data_type"))
    if fn is None:
        return n.clean(value) if isinstance(value, str) else value, None
    return fn(value)
