from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Crosstab & Pivot Specialist", "goal": "Generar tablas de contingencia y test Chi-cuadrado."},
    {"role": "Group Differences Analyst", "goal": "Comparar medias entre subgrupos mediante t-Student / ANOVA."},
    {"role": "Scatter & Bivariate Modeler", "goal": "Analizar diagramas de dispersión y relaciones no lineales."},
    {"role": "Effect Size Evaluator", "goal": "Calcular d de Cohen, Eta cuadrado y V de Cramer."},
    {"role": "Subgroup Contrast Analyst", "goal": "Detectar divergencias significativas entre segmentos."},
    {"role": "Bivariate Synthesis Agent", "goal": "Consolidar las relaciones bivariadas más relevantes."}
]

bivariate_crew = create_specialized_crew("Bivariate Crew", "groq", agents)
