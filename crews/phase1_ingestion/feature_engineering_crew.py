from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Domain Feature Creator", "goal": "Crear variables compuestas basadas en ratios de negocio."},
    {"role": "Categorical Encoder", "goal": "Generar One-Hot o Target Encoding para variables categóricas."},
    {"role": "Scaler & Normalizer", "goal": "Aplicar StandardScaler o RobustScaler a variables continuas."},
    {"role": "Interaction Term Generator", "goal": "Calcular productos cruzados y términos polinómicos."},
    {"role": "Dimensionality Reducer", "goal": "Evaluar reducción mediante PCA o selección por varianza."},
    {"role": "Feature Importance Screener", "goal": "Clasificar las features con mayor poder predictivo."}
]

feature_engineering_crew = create_specialized_crew("Feature Engineering Crew", "groq", agents)
