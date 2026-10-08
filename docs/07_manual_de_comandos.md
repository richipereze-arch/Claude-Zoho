# 07 · Manual de comandos en lenguaje natural

Ejemplos de instrucciones que Claude entiende y cómo las ejecuta. Toda escritura pasa por la previsualización y la aprobación.

## Consultas (lectura, sin aprobación)

| Dices | Claude hace |
|---|---|
| "¿Cuántos leads de Leaseback hay por estado?" | COQL `select Lead_Status, COUNT(id) from Leads where Producto = 'Leaseback' group by Lead_Status` |
| "Busca a juan.perez@empresa.cl" | `searchRecords` por email en Leads **y** Contacts |
| "Muéstrame las cuentas en Validación Compliance de Ricardo" | COQL sobre Accounts con `IBs_Atributo` y `Ejecutivo_Junior` |
| "Tratos abiertos con cierre vencido" | COQL sobre Deals con `Stage` abierto y `Closing_Date < hoy` |
| "Auditoría de calidad de Leads" | Conteos de vacíos, propietarios desactivados y teléfonos inválidos (ver `docs/01` §4) |
| "Historial del lead 6839…" | `getTimelines` |

## Cargas

| Dices | Claude hace |
|---|---|
| "Carga esta planilla como leads de la feria X, fuente Aviso, dueño Diego Vargas" | `plan --set Lead_Source=Aviso Owner=…` → búsquedas → `classify` → muestra `preview.md` y espera tu OK |
| "Agrega este prospecto: Ana Soto, Inversiones Sur SpA, +56 9 1234 5678, interesada en Mutuo" | Arma un CSV de 1 fila marcando lo confirmado → mismo flujo |
| "Del correo adjunto, crea el contacto y una tarea de seguimiento para el viernes" | Extrae datos (separando confirmados de inferidos), propone el contacto y la tarea con `Due_Date` y espera tu OK |
| "Actualiza el producto de estos 30 leads a Financiamiento" | Lee los valores actuales, muestra antes y después, y avisa de conflictos donde ya existe otro valor |
| "Agrega una nota a la cuenta X: reunión del 05/10, pidió simulación" | `createNotesModule` con `Parent_Id`, tras confirmar. No marca la reunión como realizada salvo que lo indiques |

## Calidad de datos

| Dices | Claude hace |
|---|---|
| "Encuentra posibles duplicados de leads por teléfono" | Recorre los leads por páginas, agrupa por teléfono normalizado y reporta los grupos. **No fusiona** |
| "Leads sin seguimiento hace 30 días" | COQL por `Last_Activity_Time` |
| "Leads de usuarios desactivados" | COQL por `Owner` contra los usuarios desactivados. Propone una reasignación, que requiere aprobación |

## Palabras clave de control

- **"solo simula"** → se detiene en la previsualización.
- **"aprobado"** / **"aprobado el lote"** → ejecuta los chunks mostrados, exactamente como se presentaron.
- **"con workflows"** → escribe con `trigger: ["workflow"]` (por defecto, sin automatizaciones).
- **"reanuda el lote X"** → vuelve a clasificar `runs/X`. Lo ya escrito se omite.
