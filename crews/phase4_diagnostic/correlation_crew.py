from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Pearson & Spearman Specialist", "goal": "Calcular matrices de correlación lineal y de rangos."},
    {"role": "Partial Correlation Analyst", "goal": "Evaluar correlaciones parciales controlando covariables."},
    {"role": "Multicollinearity Auditor (VIF)", "goal": "Calcular Variance Inflation Factors para detectar colinealidad."},
    {"role": "Nonlinear Association Evaluator", "goal": "Calcular información mutua (Mutual Information)."},
    {"role": "Spurious Correlation Filter", "goal": "Descartar correlaciones espurias por terceras variables."},
    {"role": "Correlation Matrix Synthesizer", "goal": "Generar resumen estructurado de las dependencias."}
]

correlation_crew = create_specialized_crew("Correlation Crew", "groq", agents)
