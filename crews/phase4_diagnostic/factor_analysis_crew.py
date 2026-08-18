from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "KMO & Bartlett Assessor", "goal": "Evaluar adecuación muestral para análisis factorial."},
    {"role": "Principal Component Extractor", "goal": "Extraer componentes principales y varianza explicada."},
    {"role": "Factor Rotation Specialist", "goal": "Aplicar rotación Varimax / Promax para interpretabilidad."},
    {"role": "Granger Causality Tester", "goal": "Evaluar causalidad en el sentido de Granger entre variables."},
    {"role": "Confounder & Mediator Mapper", "goal": "Identificar variables confusoras y mediadoras en el sistema."},
    {"role": "Causal Graph Synthesizer", "goal": "Construir grafo causal preliminar del fenómeno."}
]

factor_analysis_crew = create_specialized_crew("Factor Analysis Crew", "groq", agents)
