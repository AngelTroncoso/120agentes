from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "ROI & Business Case Modeler", "goal": "Cuantificar el retorno de inversión proyectado de las intervenciones."},
    {"role": "Implementation Roadmap Architect", "goal": "Diseñar cronograma de ejecución por fases (Corto/Mediano plazo)."},
    {"role": "Resource Allocation Strategist", "goal": "Asignar presupuestos óptimos según el impacto marginal."},
    {"role": "KPI & OKR Alignment Specialist", "goal": "Vincular las recomendaciones a métricas clave de la empresa."},
    {"role": "Change Management Assessor", "goal": "Evaluar riesgos operacionales de adopción en la organización."},
    {"role": "Executive Strategy Synthesizer", "goal": "Redactar el plan estratégico final para el C-Level."}
]

strategy_crew = create_specialized_crew("Strategy Crew", "gemini", agents)
