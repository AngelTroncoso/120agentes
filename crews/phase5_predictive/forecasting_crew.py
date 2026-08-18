from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "ARIMA / SARIMAX Specialist", "goal": "Ajustar modelos autorregresivos y de media móvil con estacionalidad."},
    {"role": "Exponential Smoothing Modeler", "goal": "Aplicar métodos Holt-Winters aditivos y multiplicativos."},
    {"role": "Machine Learning Forecaster", "goal": "Entrenar regresores con rezagos temporales y variables exógenas."},
    {"role": "Forecast Horizon Evaluator", "goal": "Calcular MAPE, WAPE y MASE en ventana out-of-time."},
    {"role": "Confidence Interval Modeler", "goal": "Construir conos de incertidumbre del 80% y 95% de confianza."},
    {"role": "Forecast Report Synthesizer", "goal": "Consolidar las proyecciones a corto y mediano plazo."}
]

forecasting_crew = create_specialized_crew("Forecasting Crew", "gemini", agents)
