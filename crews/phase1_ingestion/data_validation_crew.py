from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Schema Validator", "goal": "Verificar contratos de datos y ausencia de nulos críticos."},
    {"role": "Range & Bounds Checker", "goal": "Comprobar que los valores numéricos cumplan rangos lógicos."},
    {"role": "Referential Integrity Auditor", "goal": "Validar coherencia lógica y claves foráneas implícitas."},
    {"role": "Data Drift Detector", "goal": "Evaluar si la distribución muestral presenta sesgos."},
    {"role": "Leakage Prevention Agent", "goal": "Garantizar que no existan variables que filtren el target."},
    {"role": "Validation Sign-off Agent", "goal": "Emitir certificado de validación para pasar a Fase 2."}
]

data_validation_crew = create_specialized_crew("Data Validation Crew", "groq", agents)
