# Claude Code × Zoho CRM

Integración de Claude Code con el Zoho CRM de **Banca Inversiones** mediante el conector MCP oficial, más un motor local de carga que normaliza, valida contra el esquema real, deduplica y audita.

| Entregable | Ubicación |
|---|---|
| 1. Integración MCP operativa | Conector `Zoho_CRM` + guardas en `.claude/settings.json` |
| 2. Diagnóstico técnico | `docs/01_diagnostico_conexion_e_instancia.md` |
| 3. Diccionario de campos | `docs/02_diccionario_de_datos.md`, `schema/*.fields.json` |
| 4. Matriz de mapeo y reglas | `docs/03_mapeo_y_reglas_de_carga.md` |
| 5. Procedimiento de importación masiva | `docs/04_procedimiento_importacion_masiva.md` |
| 6. Deduplicación y validación | `docs/05_deduplicacion_y_validacion.md`, `zoho_loader/dedup.py`, `zoho_loader/schema.py` |
| 7. Reportes de auditoría | `docs/06_auditoria_seguridad_y_revision.md`, `zoho_loader/pipeline.py` |
| 8. Manual de comandos | `docs/07_manual_de_comandos.md` |

```bash
python3 -m unittest discover -s tests          # 14 tests
python3 -m zoho_loader --help
```

Requisitos: Python 3.11+ y `openpyxl` para leer Excel. Las reglas de operación del agente están en `CLAUDE.md`.
