from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Schema & Structure Analyst", "goal": "Detectar tipos de datos, nulls y consistencia de columnas."},
    {"role": "Data Quality Scorer", "goal": "Calcular score de integridad 0-100 para el dataset."},
    {"role": "Distribution Profiler", "goal": "Evaluar asimetría, curtosis y normalidad de variables."},
    {"role": "Outlier Scanner", "goal": "Escanear valores atípicos mediante el método IQR."},
    {"role": "Relationship Mapper", "goal": "Mapear correlaciones iniciales y covarianzas clave."},
    {"role": "Profiling Report Writer", "goal": "Consolidar los hallazgos en un perfil estructurado."}
]

data_profiling_crew = create_specialized_crew("Data Profiling Crew", "groq", agents)
