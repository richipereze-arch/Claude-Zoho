# 04 · Procedimiento de importación masiva

Cada lote vive en `runs/<fecha>-<módulo>-<descripción>/`. Esa carpeta **no se versiona** porque contiene datos personales.

```
[archivo] → plan → búsquedas MCP → classify → PREVISUALIZACIÓN → aprobación → escritura MCP por chunks → record → report → verify
```

## Paso a paso

1. **Recepción.** El archivo (Excel, CSV o JSON) se copia a `runs/<lote>/`. Para PDF, Word o correos, Claude extrae una tabla y la guarda como CSV en el lote, marcando lo inferido.
2. **Plan (sin tocar Zoho):**
   ```bash
   python3 -m zoho_loader plan --module Leads --input runs/<lote>/origen.xlsx \
     --source "Feria X, planilla de Juan, 2026-10-08" --run runs/<lote> \
     --set Lead_Source=Aviso Producto=Leaseback   # valores por instrucción
     # --map "Col rara=Description"   para forzar mapeos
   ```
   Revisar las columnas sin mapear y las filas con problemas.
3. **Búsquedas de deduplicación (lectura MCP).** Para cada `lookups` de `rows.json`, Claude ejecuta `searchRecords` (email, teléfono, palabra o criterio). Pide solo los campos necesarios y guarda `runs/<lote>/candidates.json` = `{row_key: [registros con "_module"]}`. Para lookups de cuenta, agrega `"_accounts": {"Nombre": "id"}`.
4. **Clasificación:**
   ```bash
   python3 -m zoho_loader classify --run runs/<lote> --candidates runs/<lote>/candidates.json
   ```
   Genera `plan.json` (chunks de ≤100 listos para la API) y `preview.md` (resumen de nuevos, actualizaciones, duplicados, errores y conflictos).
5. **Aprobación.** Claude presenta la previsualización y espera aprobación **del lote completo**. Las filas en *revisar* o *error* no se escriben. Se resuelven y se replanifican.
6. **Escritura.** Por cada chunk, Claude llama `createRecords` / `updateRecords` con `body` del chunk y `trigger` según lo aprobado (por defecto `[]`). La respuesta se guarda en `runs/<lote>/resp_<n>.json` y se registra:
   ```bash
   python3 -m zoho_loader record --run runs/<lote> --chunk <n> --response runs/<lote>/resp_<n>.json
   ```
7. **Reanudación.** Si algo se interrumpe, al volver a ejecutar `classify` las filas ya registradas como creadas o actualizadas quedan en *omitir* (idempotencia por `row_key` = hash del registro normalizado).
8. **Conciliación.** Claude relee los IDs escritos (`getRecords ids=...`), guarda `fetched.json` = `{id: registro}` y ejecuta:
   ```bash
   python3 -m zoho_loader verify --run runs/<lote> --fetched runs/<lote>/fetched.json
   python3 -m zoho_loader report --run runs/<lote>
   ```

## Límites y buenas prácticas

- Máximo 100 registros por llamada y 200 por página de lectura. `searchRecords` puede tardar en indexar registros recién creados, así que **no se debe repetir un lote recién cargado sin pasar por `record`**.
- Cargas de más de 2.000 filas: dividirlas en sublotes y aprobar cada uno.
- `Owner` explícito por fila o lote. Si se omite, queda a nombre del usuario conectado.

## Regenerar el esquema tras cambios en el CRM

Claude ejecuta `getFields` y `getLayouts` por módulo, guarda las salidas como `<Módulo>.json` y `L_<Módulo>.json` en una carpeta temporal y luego corre:
```bash
python3 tools/build_dictionary.py <carpeta_meta> .
```
Eso actualiza `schema/*.fields.json` y `docs/02_diccionario_de_datos.md`.
