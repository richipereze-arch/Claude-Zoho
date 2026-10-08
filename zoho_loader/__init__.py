"""Motor de carga para Zoho CRM: normaliza, valida contra el esquema real, deduplica y audita.

La E/S con Zoho la ejecuta Claude mediante el conector MCP oficial; este paquete solo prepara
planes, clasifica coincidencias y registra auditoría. Nunca maneja credenciales.
"""
