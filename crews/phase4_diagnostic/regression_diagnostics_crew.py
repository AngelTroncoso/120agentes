from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Residual Normality Checker", "goal": "Ejecutar prueba de Jarque-Bera y Shapiro-Wilk sobre residuos."},
    {"role": "Heteroskedasticity Tester", "goal": "Ejecutar prueba de Breusch-Pagan y White para heterocedasticidad."},
    {"role": "Autocorrelation Diagnostic Agent", "goal": "Calcular estadístico Durbin-Watson y Breusch-Godfrey."},
    {"role": "Influence & Leverage Analyst", "goal": "Calcular distancias de Cook y puntos de alto apalancamiento."},
    {"role": "Functional Form Tester (RESET)", "goal": "Ejecutar test RESET de Ramsey para especificación correcta."},
    {"role": "Econometric Diagnostic Reporter", "goal": "Consolidar el diagnóstico de robustez de los modelos."}
]

regression_diagnostics_crew = create_specialized_crew("Regression Diagnostics Crew", "groq", agents)
