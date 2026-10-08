# 03 · Matriz de mapeo y reglas de carga

La fuente de verdad del esquema es `schema/<Módulo>.fields.json`, generado desde la metadata real. Para regenerarlo después de un cambio en el CRM, ver `docs/04`.

## Clasificación de cada dato

| Clase | Significado | Cómo se registra |
|---|---|---|
| **confirmado** | Viene literalmente de la fuente (celda, texto o correo) | `provenance[campo] = "confirmado"` |
| **instrucción** | Lo indicó el usuario para el lote (`--set Lead_Source=Aviso`) | `provenance[campo] = "instrucción"` |
| **inferido** | Deducido por Claude a partir de texto libre | Solo se propone en la previsualización. **No se escribe sin confirmación** |
| **desconocido** | No está en la fuente | Queda vacío. Si es obligatorio, la fila pasa a *error* y se reporta antes de crear |

Nunca se rellenan campos para "pasar" una validación.

## Matriz por módulo (campos clave)

### Leads (Posibles clientes) · layout `Standard` `6839037000000091055`

| Dato de origen (alias aceptados) | API name | Regla |
|---|---|---|
| nombre completo, nombre y apellido | `Last_Name` (oblig.) | En este CRM el nombre completo va en `Last_Name`. Se normaliza la capitalización |
| empresa, compañía, razón social, nombre cuenta | `Company` (oblig. layout) | Si es una persona natural sin empresa, **preguntar** qué usar; no se inventa |
| correo, email, mail | `Email` | Minúsculas y validación de formato. Si es inválido, se descarta y se reporta |
| teléfono, fono | `Phone` | E.164 `+56XXXXXXXXX`. Si hay 8 dígitos sin prefijo, es ambiguo y se rechaza |
| celular, móvil, whatsapp | `Mobile` | Ídem |
| producto | `Producto` | Picklist: Trading, Mutuo, AFI, Leaseback, Departamento, Financiamiento, Venta Propiedad, IB |
| estado | `Lead_Status` | Picklist (8 valores) |
| fuente, origen | `Lead_Source` | Picklist. Hoy está vacío en el 99,7 %: **se recomienda exigirlo en cada lote** con `--set` |
| atributo | `Atributo_del_Prospecto` | Picklist (embudo FinanciaK) |
| fase | `Fase_FinanciaK` | Fase 1–4, Concluido, Caído |
| ejecutivo, ejecutivo junior | `Ejecutivo_Junior` | Picklist de **texto** (no es un usuario) |
| analista | `Analista_de_Inversiones` | Picklist de texto |
| broker | `Broker_FK` | Picklist de texto |
| comuna | `Comuna_Ciudad` | Picklist de comunas |
| propietario, responsable | `Owner` | Se resuelve contra `schema/users.json`, solo usuarios activos. Si se omite, Zoho asigna al usuario conectado |
| observaciones, comentarios, descripción | `Description` | Texto libre |

### Contacts (en la práctica IBs / Brokers) · layout `6839037000000091033`

Obligatorios: `Last_Name`, `Mobile`, `Producto`, `Atributo_IB`. `Email` es **único** en el CRM. `Account_Name` es lookup y se resuelve a ID buscando la cuenta. `RUT` es opcional: solo se carga si existe un uso legítimo documentado.

### Accounts (clientes) · layout `6839037000000091029`

Obligatorios de layout: `Account_Name`, `RUT`, `Phone`, `Rating`, `Account_Type`, `Producto`, `IBs_Atributo`, `Ejecutivo_Junior`, `Analista_de_Inversiones`. Ver la decisión pendiente sobre RUT en `docs/01` §4.

### Deals (operaciones) · layout `6839037000000091023`

Obligatorios: `Deal_Name`, `Account_Name` (lookup, se resuelve a ID), `Type`, `Closing_Date`, `Stage`, `Producto`, `Analista_de_Inversiones`. `Amount` en CLP salvo que se indique USD (`Currency`).

### Tasks

| Campo | API | Regla |
|---|---|---|
| Asunto | `Subject` (oblig.) | Texto (el picklist es solo sugerencia) |
| Vencimiento | `Due_Date` | ISO `YYYY-MM-DD` |
| Contacto / lead | `Who_Id` | Lookup por ID |
| Relacionado con | `What_Id` + `$se_module` | Lookup por ID al módulo correspondiente |
| Estado | `Status` | No iniciado, Aplazados, En curso, Completado, En espera de entrada. **Nunca "Completado" sin respaldo** |
| Prioridad | `Priority` | Alto, Más alto, Normal, Bajo, Más bajo |

### Notes

`Note_Title`, `Note_Content`, `Parent_Id` = `{module: {api_name}, id}`. Las notas registran solo hechos aportados por la fuente.

## Reglas de normalización (`zoho_loader/normalize.py`)

| Tipo | Regla |
|---|---|
| Teléfono | E.164. Acepta `9 1234 5678`, `56912345678`, `+56 2 2xxx xxxx`, `0056...`. Los extranjeros con `+` se conservan. Si hay 8 dígitos sin prefijo, se rechaza |
| Correo | `lower()`, sin `mailto:`, validación de formato |
| Fecha | ISO. Se asume **día/mes** (formato chileno), nunca mes/día |
| Monto | `$1.234.567`, `1.234,50`, `USD 1,500.25` → número |
| Moneda | Solo CLP y USD (las habilitadas en el CRM). Cualquier otra genera error |
| Nombres de persona | Capitalización correcta solo si venían en MAYÚSCULAS o minúsculas |
| Razón social | Se conserva tal cual. La **clave de comparación** quita tildes, puntuación y sufijos (SpA, S.A., Ltda., EIRL...) |
| RUT | Validación del dígito verificador y formato `12.345.678-5`. Es dato restringido y se enmascara en logs |
| Picklists | Coincidencia sin distinguir mayúsculas ni tildes contra etiqueta o valor interno. Se envía la etiqueta exacta |
| Texto | Recorte de espacios y validación del largo máximo del campo |
