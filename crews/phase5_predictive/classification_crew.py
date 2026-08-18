from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Logistic Regression Specialist", "goal": "Entrenar y calibrar modelos logísticos lineales."},
    {"role": "Gradient Boosting Engineer", "goal": "Optimizar XGBoost / LightGBM con búsqueda de hiperparámetros."},
    {"role": "Random Forest Modeler", "goal": "Construir ensembles de Random Forest para robustez."},
    {"role": "ROC-AUC & PR Evaluator", "goal": "Evaluar curvas ROC, Precision-Recall y matrices de confusión."},
    {"role": "SHAP & Interpretability Agent", "goal": "Calcular valores SHAP globales y locales por feature."},
    {"role": "Champion Model Selector", "goal": "Seleccionar y serializar el modelo campeón según F1 y AUC."}
]

classification_crew = create_specialized_crew("Classification Crew", "gemini", agents)
