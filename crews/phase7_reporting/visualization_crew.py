from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Chart Selection Specialist", "goal": "Elegir el tipo de gráfico óptimo para cada tipo de hallazgo."},
    {"role": "Color Palette & Aesthetic Designer", "goal": "Garantizar contraste, accesibilidad y armonía visual."},
    {"role": "Plotly & D3 Code Generator", "goal": "Generar especificaciones interactivas de gráficos en JSON/HTML."},
    {"role": "KPI Card & Gauge Designer", "goal": "Diseñar tarjetas métricas de alto impacto visual."},
    {"role": "Visual Narrative Flow Architect", "goal": "Ordenar la secuencia visual para facilitar la comprensión."},
    {"role": "Visual Dashboard Assembler", "goal": "Consolidar el bundle de visualizaciones listas para el reporte."}
]

visualization_crew = create_specialized_crew("Visualization Crew", "groq", agents)
