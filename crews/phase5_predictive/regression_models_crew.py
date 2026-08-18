from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Ridge & Lasso Regularizer", "goal": "Entrenar modelos regularizados L1 y L2 para penalización."},
    {"role": "Nonlinear Regressor (GBDT)", "goal": "Ajustar árboles de regresión LightGBM / CatBoost."},
    {"role": "Quantile Regressor", "goal": "Modelar cuantiles 10%, 50% y 90% para intervalos de predicción."},
    {"role": "RMSE & R2 Auditor", "goal": "Evaluar métricas de error cuadrático y varianza explicada."},
    {"role": "Residual Distribution Evaluator", "goal": "Comprobar homocedasticidad y media cero en residuos."},
    {"role": "Regression Model Exporter", "goal": "Generar funciones matemáticas para inferencia en producción."}
]

regression_models_crew = create_specialized_crew("Regression Models Crew", "gemini", agents)
