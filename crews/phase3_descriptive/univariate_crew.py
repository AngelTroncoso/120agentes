from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Central Tendency Analyst", "goal": "Calcular media, mediana, moda y medias recortadas."},
    {"role": "Dispersion Specialist", "goal": "Evaluar desviación estándar, varianza, rango intercuartílico."},
    {"role": "Shape & Skewness Assessor", "goal": "Analizar coeficiente de asimetría de Fisher y curtosis."},
    {"role": "Categorical Frequency Analyst", "goal": "Obtener tablas de frecuencias relativas y modas."},
    {"role": "Density Estimator", "goal": "Modelar funciones de densidad empírica (KDE)."},
    {"role": "Univariate Summary Writer", "goal": "Redactar resumen narrativo univariado con hallazgos clave."}
]

univariate_crew = create_specialized_crew("Univariate Crew", "groq", agents)
