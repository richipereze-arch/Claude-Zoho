# Agente Zoho CRM — Banca Inversiones

Este repositorio convierte a Claude Code en el operador de datos del Zoho CRM de Banca Inversiones, a través del **conector MCP oficial `Zoho_CRM`**.

## Reglas de operación (obligatorias)

1. **Consulta → propone → ejecuta.** La lectura está autorizada. Toda escritura pasa por `python3 -m zoho_loader` (plan → classify → preview) y requiere aprobación explícita del lote completo.
2. **Nunca** eliminar, fusionar, cambiar permisos ni la estructura del CRM. Esas herramientas están bloqueadas en `.claude/settings.json`.
3. **No inventar datos.** Distinguir confirmado, instrucción, inferido y desconocido. Si falta un obligatorio, reportarlo antes de crear.
4. **No sobrescribir** valores distintos: solo completar vacíos y reportar conflictos.
5. Escribir con `trigger: []` salvo que el usuario apruebe automatizaciones para ese lote.
6. No marcar llamadas, reuniones, tareas ni ventas como realizadas sin respaldo.
7. RUT/RUN: nunca exigirlo por defecto. Es dato restringido, se enmascara y no se pide en búsquedas salvo uso legítimo.
8. Datos personales solo en `runs/` (ignorado por git). Nunca escribir credenciales ni tokens.
9. Usar el esquema real (`schema/*.fields.json`, `docs/02`). Si el CRM cambió, regenerarlo (`docs/04`).
10. En búsquedas, pedir solo los campos necesarios (`fields=`).

## Mapa del repo

- `docs/01` diagnóstico · `docs/02` diccionario · `docs/03` mapeo · `docs/04` importación · `docs/05` deduplicación · `docs/06` auditoría y seguridad · `docs/07` manual de comandos
- `zoho_loader/` motor (normalize, schema, mapping, dedup, pipeline, CLI)
- `schema/` esquema real exportado más `users.json`
- `tools/build_dictionary.py` regenera esquema y diccionario
- Tests: `python3 -m unittest discover -s tests`
