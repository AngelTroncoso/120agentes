from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Missing Value Imputer", "goal": "Determinar estrategia de imputación (media, mediana, KNN o moda)."},
    {"role": "Duplicate Deduplicator", "goal": "Identificar y depurar registros duplicados exactos o difusos."},
    {"role": "Outlier Treatment Specialist", "goal": "Aplicar winsorización o filtrado a valores atípicos severos."},
    {"role": "Data Type Converter", "goal": "Convertir tipos categóricos, numéricos y fechas estandarizadas."},
    {"role": "String Normalizer", "goal": "Estandarizar cadenas de texto, eliminar espacios y acentos."},
    {"role": "Clean Data Certifier", "goal": "Verificar la integridad final del dataset limpio."}
]

data_cleaning_crew = create_specialized_crew("Data Cleaning Crew", "groq", agents)
