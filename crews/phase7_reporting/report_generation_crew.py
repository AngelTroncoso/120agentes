from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Executive Summary Writer", "goal": "Redactar resumen ejecutivo condensado de 1 página para directivos."},
    {"role": "Methodology Documenter", "goal": "Documentar la trazabilidad de algoritmos y pruebas estadísticas."},
    {"role": "Findings & Insights Synthesizer", "goal": "Explicar los hallazgos principales con lenguaje de negocio."},
    {"role": "Recommendation & Action Plan Writer", "goal": "Detallar los pasos prescriptivos priorizados por impacto."},
    {"role": "HTML & CSS Layout Architect", "goal": "Construir documento HTML moderno, responsivo y profesional."},
    {"role": "Final Quality & Polish Auditor", "goal": "Revisar ortografía, cohesión y emitir el reporte final definitivo."}
]

report_generation_crew = create_specialized_crew("Report Generation Crew", "groq", agents)
