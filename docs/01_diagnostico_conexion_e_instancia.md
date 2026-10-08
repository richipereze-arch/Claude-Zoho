# 01 · Diagnóstico de conexión e instancia

Fecha: 2026-10-08 · Modo: **solo lectura** (no se creó, modificó ni eliminó ningún registro).

## 1. Conectividad (Fase 1)

| Ítem | Resultado |
|---|---|
| Conector | **MCP oficial de Zoho CRM** (`Zoho_CRM`), ya configurado y operativo en este entorno de Claude Code. No se construyó infraestructura paralela. |
| Autenticación | OAuth 2.0 gestionado por el conector. Ningún token pasa por la conversación, los logs ni el repositorio. |
| Centro de datos | Resuelto por el conector. La organización opera en zona horaria `America/Santiago`, moneda base CLP. |
| Usuario conectado | **Ricardo Perez Elmohrez** · perfil **Standard** · rol *Ejecutivo Fija / Deuda*. Toda lectura y escritura queda limitada por los permisos de este perfil y a su nombre en el CRM. |
| API utilizada | Zoho CRM REST API v8 (a través del conector). |

### Herramientas disponibles en el conector (44)

| Categoría | Herramientas | Uso en este proyecto |
|---|---|---|
| Metadata | `getOrganization`, `getModules`, `getModuleByApiName`, `getFields`, `getLayouts`, `getLayoutById`, `getRelatedLists`, `getAssignmentRules`, `getAllTerritories`, `getVariables`, `getTags`, `getUsers`, `getSingleUser` | Reconocimiento y diccionario |
| Lectura de datos | `getRecords`, `getRecord`, `searchRecords`, `executeCOQLQuery`, `getRelatedRecords`, `getRelatedRecord`, `getTimelines`, `getBulkReadJobDetails` | Deduplicación, calidad y conciliación |
| Escritura | `createRecords`, `updateRecord(s)`, `upsertRecords`, `createNotesModule`, `updateNotesModule`, `updateRelatedRecords`, `updateSpecificRelatedRecord`, `createTags`, `postAddTags` | Solo con aprobación (ver `.claude/settings.json` → `ask`) |
| Destructivas o estructurales | `deleteRecord(s)`, `deleteNotesModule`, `delinkSpecificRelatedRecord`, `createFields`, `updateUser`, `updateSingleUser`, `updateVariableById`, `convertInventory` | **Bloqueadas** en `.claude/settings.json` → `deny` |

### Pruebas de conectividad ejecutadas (Fase 9, pasos 1–5)

| # | Prueba | Herramienta | Resultado |
|---|---|---|---|
| 1 | Conexión al CRM | `getOrganization` | ✅ |
| 2 | Consulta de organización | `getOrganization` | ✅ Banca Inversiones, org `6839037000000020005`, producción, edición Standard pagada (13 licencias, vence 2027-06-10), CLP + USD |
| 3 | Listado de módulos | `getModules` | ✅ 54 módulos, sin módulos personalizados |
| 4 | Consulta de campos y layouts | `getFields`, `getLayouts` | ✅ Leads, Contacts, Accounts, Deals y Tasks |
| 5 | Búsqueda de registros | `searchRecords` (email, teléfono, criterio), `getRecords`, COQL | ✅ |
| 6 | Mapeo de datos de ejemplo | `zoho_loader plan` | ✅ ver `runs/` (local) y §5 |
| 7 | Simulación sin escritura | `zoho_loader classify` con candidatos reales | ✅ ver §5 |

### Brechas de capacidad del conector

- **No hay herramientas para leer Workflows, Blueprints, reglas de validación personalizadas, funciones ni reglas de duplicidad del CRM.** Ese inventario debe hacerlo un administrador desde *Configuración → Automatización*. Mientras tanto, la política es escribir con `trigger: []` (sin automatizaciones) salvo aprobación explícita. Ver §4.
- No hay `bulk write` (importación masiva por archivo). Las cargas se hacen en lotes de 100 registros con `createRecords` / `updateRecords`, que basta para el volumen actual.
- No hay conversión de Leads (`convertLead`). Si se necesita, se puede complementar con la REST API v8 directa, pero eso requeriría credenciales OAuth propias. No se recomienda por ahora.

## 2. Organización y usuarios

17 usuarios: 13 activos y 4 desactivados.

| Usuario | Rol | Perfil | Estado |
|---|---|---|---|
| Rodrigo Martori | CEO | Administrator | activo |
| Camilo Bravo | Jefes Comerciales | Administrator | activo |
| Tamara Rojas | Jefes Comerciales | Standard | activo |
| Marcelo Correa | Jefes Fija / Deuda | Standard | activo |
| Sebastián Sergio Méndez Estay | Jefes Fija / Deuda | Standard | activo |
| Daniel Larrain Elias | Jefes Fija / Deuda | Standard | activo |
| Rommy Fernanda Leiva Lopez | Ejecutivo Fija / Deuda | Standard | activo |
| Ricardo Perez Elmohrez | Ejecutivo Fija / Deuda | Standard | activo (usuario del conector) |
| Andrés Bilbao Bilbao | Ejecutivo Fija / Deuda | Standard | activo |
| Hari Saits | Ejecutivos y Analistas | Standard | activo |
| Matias Sandoval | Ejecutivos y Analistas | Standard | activo |
| Diego Vargas | Ejecutivos y Analistas | Standard | activo |
| Rodrigo Quintana | Ejecutivos y Analistas | Standard | activo |
| Luciano Pellegrini | Jefes Comerciales | Standard | **desactivado** |
| Felipe Norese | Ejecutivos y Analistas | Standard | **desactivado** |
| Johnny Hernández | Ejecutivos y Analistas | Standard | **desactivado** |
| Marcelo Hernández Gálvez | Ejecutivos y Analistas | Standard | **desactivado** |

Los IDs están en `schema/users.json`, que el motor usa para resolver propietarios. Solo se asignan usuarios activos.

## 3. Volumen y procesos comerciales

Conteos visibles para el usuario conectado:

| Módulo | Registros | Notas |
|---|---|---|
| Leads (Posibles clientes) | 14.002 | Ingreso activo: hay altas automáticas el mismo día de esta auditoría |
| Contacts | 513 | En la práctica funcionan como **IBs / Brokers** (campos `Atributo_IB`, `Contrato_IB`, `Atributo_Broker_FK`) |
| Accounts (Cuentas) | 424 | Funcionan como **clientes inversionistas** (RUT, contratos, `IBs_Atributo` = "Etapa del Cliente") |
| Deals (Tratos) | 759 | 742 *Cerrado ganado*, 15 *Clasificación*, 1 *Negociación/revisión*, 1 *Cerrado perdido*. Se usan como **registro de operaciones** (comprobantes de depósito y rescate), no como embudo |
| Tasks | 268 | 262 completadas, 6 no iniciadas |

Productos de negocio (picklist `Producto`): Trading, Mutuo, AFI, Leaseback, Departamento, Financiamiento, Venta Propiedad, IB.

Etapas del cliente en Accounts (`IBs_Atributo`): Deposito Recibido → Contratos Firmados → Credenciales Enviadas + Forms → Validación Compliance → Habilitación de Cuenta → Traspaso a Post Venta (más Reversado a Ejecutivo, Avanzado, Inseguro, Referido).

Embudo FinanciaK en Leads: `Atributo_del_Prospecto` (Interesado → Enviar Simulación → Simulación Enviada → Recopilación de documentos → Presentar a comité → Comité aprueba/no aprueba → Enviado a EETT → Borradores Listos → Firmado) y `Fase_FinanciaK` (Fase 1–4, Concluido, Caído).

Relaciones: Contacts → Accounts (`Account_Name`), Deals → Accounts (`Account_Name`, obligatorio) y Contacts (`Contact_Name`), Tasks → Contact/Lead (`Who_Id`) y cualquier módulo (`What_Id`).

## 4. Hallazgos, inconsistencias y oportunidades (sin modificar nada)

### Críticos para la carga

1. **El RUT es obligatorio por layout en Accounts** (`RUT`, "RUT Cliente"). Esto choca con la regla de no exigir RUT por defecto. Hay que crear Cuentas con RUT, pedir al administrador que lo haga opcional, o usar otro layout. Además, 65 cuentas ya existen sin RUT, así que la obligatoriedad se agregó después o se omite en algunas vías de ingreso. **Decisión pendiente.**
2. **Obligatorios de layout más estrictos que el sistema:** Accounts exige 9 campos (`Account_Name`, `RUT`, `Phone`, `Rating`, `Account_Type`, `Producto`, `IBs_Atributo`, `Ejecutivo_Junior`, `Analista_de_Inversiones`). Deals exige 7. Contacts exige `Mobile`, `Producto` y `Atributo_IB`. Leads exige `Last_Name` y `Company`. El motor los valida antes de escribir.
3. **Automatizaciones desconocidas:** no se pueden auditar con este conector y este perfil. Hay altas automáticas recientes en Leads (otra integración o formulario). Política propuesta: `trigger: []` en la prueba y decisión explícita para cargas reales.
4. **`Leads.Email` no es único** (en Contacts sí). Un lead se puede duplicar con el mismo correo, y la deduplicación del motor es la única barrera.
5. **Valores de picklist con etiqueta distinta del valor interno** (por ejemplo, `Rating` "Interesado en Financiamiento" = `Acquired`, y `Lead_Status` "Contactado" = `Contacted`). La API devuelve la etiqueta visible. El motor envía la etiqueta visible exacta. Se confirma en la prueba real.

### Calidad de datos

| Hallazgo | Medición |
|---|---|
| Leads sin `Lead_Status` | 13.578 de 14.002 (97 %) |
| Leads sin `Lead_Source` | 13.963 (99,7 %) |
| Leads sin producto (`null` o "-") | 8.517 (61 %) |
| Leads sin correo | 273 |
| Leads sin ningún correo ni teléfono | 45 |
| Leads cuyo propietario está desactivado | 364 (Norese 188, J. Hernández 88, M. Hernández Gálvez 88) |
| Teléfonos en formatos mixtos | con y sin `+56`, en `Phone` o `Mobile` indistintamente |
| Teléfonos de relleno | p.ej. `+56987654321` compartido por leads distintos, uno con nombre ficticio |
| Contacts sin Cuenta | 387 de 513 (75 %) |
| Accounts sin RUT pese a ser obligatorio | 65 |
| Deals abiertos con fecha de cierre vencida | 16 |
| Tareas abiertas | 6 |

### Diseño del CRM (oportunidades de mejora, para decisión del administrador)

- Las personas se registran como **picklists de texto**, no como usuarios: `Ejecutivo_Junior`, `Analista_de_Inversiones`, `IBs`, `Broker_FK`, `Sub_IB_s`. Los nombres no coinciden con la lista de usuarios (p.ej. "Marcelo Henandez") e incluyen personas inactivas. Esto impide reportes por usuario y se desalinea con `Owner`.
- Campos estándar reetiquetados que conservan valores heredados: `Industry` → "Sub IB´s" (mezcla un nombre de persona con "ERP", "ASP"...), `Account_Type` → "Modalidad de Operación" (Manual/MAM/BOT junto a Competidor/Prensa...), `Rating` → "Calificación FK" / "Calificación".
- `Leads.Last_Name` se llama "Nombre Completo": el nombre completo va en `Last_Name`.
- `Contacts.Ciudad_Comuna` se llama "Región Broker" y mezcla regiones con comunas.
- No hay reglas de asignación de Leads.
- Las etapas de Deals son las genéricas de Zoho y no reflejan el proceso real (que vive en `IBs_Atributo` y `Atributo_del_Prospecto`).

## 5. Simulación sin escritura (Fase 9, pasos 6–7)

Se planificó `tests/fixtures/leads_ejemplo.csv` (3 filas ficticias) y se consultaron sus correos y teléfonos en el CRM real.

| Fila | Resultado | Motivo |
|---|---|---|
| 2 | **revisar** (posible duplicado) | El teléfono coincide con 2 leads reales de nombre distinto. **No se fusiona ni actualiza.** |
| 3 | **error** | Correo inválido y falta `Company` (obligatorio de layout). No se crea. |
| 4 | **revisar** | Producto "Criptomonedas" no existe en el picklist, y además coincide el teléfono. |

La normalización funcionó: `9 8765 4321` → `+56987654321`, `JUAN PÉREZ SOTO` → `Juan Pérez Soto`, `leaseback` → `Leaseback`. La columna desconocida se ignoró y se reportó.
