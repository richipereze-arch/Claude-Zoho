# 05 · Sistema de deduplicación y validación

## Validación previa (`zoho_loader/schema.py`)

Para cada fila se valida, contra el esquema real:

1. Que el campo exista en el módulo y sea escribible por API (excluye fórmulas y campos de sistema).
2. Que el valor de picklist o multiselect exista. Se convierte a la etiqueta exacta.
3. Que se respete el largo máximo.
4. Que estén **todos los obligatorios de sistema y de layout**. Si falta uno, la fila queda en *error* antes de crear.

## Búsqueda de candidatos (`dedup.lookup_queries`)

| Módulo | Identificadores consultados |
|---|---|
| Leads / Contacts | Correo en **Leads y Contacts**. Teléfono y móvil (últimos 9 dígitos) en ambos. Nombre si no hay otro identificador |
| Accounts | RUT (solo si viene y se autorizó su uso) y razón social normalizada |
| Deals | Nombre del trato (más la cuenta en la clasificación) |

## Clasificación (`dedup.classify`)

| Estado | Regla | Acción |
|---|---|---|
| **existente** | Exactamente **una** coincidencia fuerte: mismo correo, o mismo teléfono con nombre ≥ 0,85 similar (Leads/Contacts); mismo RUT o razón social normalizada idéntica (Accounts); mismo nombre de trato y cuenta (Deals) | Actualización conservadora |
| **posible_duplicado** | Solo coincidencias débiles: mismo teléfono con nombre distinto, nombre muy similar, razón social ≥ 0,88 similar, o la persona ya existe en el *otro* módulo (lead que ya es contacto) | *revisar*: no se escribe |
| **ambiguo** | Más de una coincidencia fuerte, o una fuerte acompañada de débiles con otros IDs | *revisar*: no se escribe |
| **nuevo** | Sin coincidencias | Se crea si pasa la validación |

Variantes de razón social: `Inversiones Ñuñoa SpA` = `INVERSIONES ÑUÑOA S.p.A.` (sin tildes, sin puntuación y sin sufijo societario).

## Actualización conservadora (`dedup.merge_update`)

- Solo se **completan campos vacíos** en el CRM.
- Si el CRM tiene un valor distinto, **no se sobrescribe**: se reporta como *conflicto* (campo, valor CRM, valor fuente) para decisión humana.
- `Owner` nunca se cambia salvo instrucción explícita.
- No se fusionan registros. Las fusiones las decide y ejecuta una persona en Zoho.

## Upsert

`upsertRecords` con `duplicate_check_fields` solo es seguro con un campo **único** configurado. En este CRM, el único campo único de los módulos clave es `Contacts.Email`. Por eso:

- **Contacts:** se puede usar upsert por `Email` si el lote viene de una fuente confiable y ya pasó por la clasificación.
- **Leads, Accounts, Deals:** no hay campo único, así que se usa el flujo search → classify → create/update. Si se quiere upsert por RUT en Accounts, el administrador debe marcar `RUT` como único (decisión de negocio y de datos personales).
