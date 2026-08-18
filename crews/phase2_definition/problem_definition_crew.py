from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Business Question Interpreter", "goal": "Traducir la pregunta del usuario en objetivos analíticos formales."},
    {"role": "Target Variable Identifier", "goal": "Identificar y validar la variable dependiente (target)."},
    {"role": "Problem Classifier", "goal": "Clasificar el problema (Regresión, Clasificación, Forecasting o Segmentación)."},
    {"role": "Hypothesis Formulator", "goal": "Formular hipótesis nulas (H0) y alternativas (H1) comprobables."},
    {"role": "Success Metrics Architect", "goal": "Definir métricas de evaluación (RMSE, F1-Score, ROI, Silhouette)."},
    {"role": "Analysis Plan Synthesizer", "goal": "Diseñar la hoja de ruta de análisis para las siguientes fases."}
]

problem_definition_crew = create_specialized_crew("Problem Definition Crew", "openrouter", agents)
