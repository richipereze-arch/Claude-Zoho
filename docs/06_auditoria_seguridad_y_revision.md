# 06 · Auditoría, seguridad y revisión independiente

## Reporte por operación (Fase 7)

Cada escritura registrada con `zoho_loader record` agrega una línea a `runs/<lote>/audit.jsonl`:

| Campo | Contenido |
|---|---|
| `timestamp` | Fecha y hora de ejecución (America/Santiago) |
| `source` | Fuente declarada del lote |
| `module`, `record_id` | Módulo intervenido e ID devuelto por Zoho |
| `source_row`, `row_key` | Fila de origen y clave de idempotencia |
| `result` | creado / actualizado / error. *omitido* y *pendiente* aparecen en `report.md` |
| `fields`, `values` | Campos modificados y valores nuevos (**enmascarados**: RUT `***8-5`, correo `ju***@dominio`, teléfono `+569****21`) |
| `conflicts` | Valor CRM frente a valor fuente no aplicado (enmascarado) |
| `zoho` | Código y mensaje devueltos por Zoho |

`report.md` consolida el lote. Antes de escribir, `preview.md` resume nuevos, actualizaciones, duplicados, errores y conflictos. `written.json` guarda localmente lo escrito sin enmascarar, solo para conciliar.

## Controles de seguridad (Fase 6)

| Control | Implementación |
|---|---|
| Consultar → proponer → ejecutar | El flujo de `docs/04` obliga a pasar por la previsualización |
| Aprobación de escrituras | `.claude/settings.json` → `ask` en toda herramienta de escritura del conector |
| Sin eliminaciones ni cambios estructurales | `.claude/settings.json` → `deny` en `delete*`, `delink*`, `createFields`, `updateUser*`, `updateVariableById`, `convertInventory` |
| Sin automatizaciones no deseadas | `trigger: []` por defecto. Activar workflows o blueprints requiere aprobación explícita del lote |
| Sin sobrescritura silenciosa | `merge_update` solo completa vacíos y reporta conflictos |
| Sin actividades falsas | No se crean llamadas, reuniones ni tareas *Completado* sin respaldo en la fuente |
| Credenciales | OAuth gestionado por el conector MCP. No hay tokens en código, logs ni repo. `.gitignore` excluye `.env`, `*.token` y `*secret*` |
| Datos personales | `runs/` no se versiona, los logs van enmascarados y las búsquedas piden solo los campos necesarios. El RUT es opcional por defecto y se trata como dato restringido |
| Mínimo privilegio | El conector opera con el perfil Standard del usuario conectado, no con un administrador |

## Revisión por roles (Fase 8)

Se ejecutó secuencialmente; no se crearon agentes paralelos.

| Rol | Revisión | Resultado |
|---|---|---|
| **Arquitecto de integración** | Conector oficial operativo, OAuth delegado, API v8, sin infraestructura paralela. Brechas: no se leen workflows ni reglas de duplicidad, no hay bulk write ni conversión de leads | ✅ Apto. Las brechas están documentadas en `docs/01` §1 |
| **Ingeniero de datos** | Normalización probada (14 tests), mapeo derivado del esquema real, deduplicación entre Leads y Contacts, idempotencia por hash | ✅ Apto. Riesgo residual: retraso de indexación en `searchRecords` justo después de cargar |
| **Especialista CRM** | Los módulos se usan con semántica propia (Contacts = IBs, Accounts = clientes, Deals = operaciones). Hay picklists de personas en vez de usuarios y etapas genéricas de Deals | ⚠️ Hay decisiones de negocio pendientes (`docs/01` §4) |
| **Auditor de calidad** | La simulación con candidatos reales clasificó bien los duplicados por teléfono de relleno. `verify` compara lo escrito contra lo releído | ✅ Apto. Falta la prueba de escritura real |
| **Auditor de seguridad y cumplimiento** | Destructivas bloqueadas, escrituras con aprobación, enmascarado y datos personales fuera del repo. RUT obligatorio en Accounts en conflicto con la política de minimización | ⚠️ Requiere decisión sobre RUT y revisión de automatizaciones por un administrador |
