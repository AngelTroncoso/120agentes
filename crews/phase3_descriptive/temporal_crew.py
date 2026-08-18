from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Trend Detector", "goal": "Identificar tendencias seculares lineales y polinómicas."},
    {"role": "Seasonality Decomposer", "goal": "Descomponer estacionalidad aditiva y multiplicativa."},
    {"role": "Autocorrelation Analyst", "goal": "Calcular funciones ACF y PACF para rezagos temporales."},
    {"role": "Stationarity Tester", "goal": "Ejecutar pruebas Augmented Dickey-Fuller (ADF) y KPSS."},
    {"role": "Structural Break Detector", "goal": "Detectar quiebres estructurales en la serie de tiempo."},
    {"role": "Temporal Reporter", "goal": "Sintetizar la dinámica temporal de las variables."}
]

temporal_crew = create_specialized_crew("Temporal Crew", "groq", agents)
