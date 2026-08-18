from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Monte Carlo Simulator", "goal": "Ejecutar 10,000 iteraciones estocásticas con variables aleatorias."},
    {"role": "Value at Risk (VaR) Analyst", "goal": "Calcular percentiles de riesgo P10, P50 y P90."},
    {"role": "Decision Tree Optimizer", "goal": "Construir árboles de decisión con valores esperados condicionales."},
    {"role": "Trade-off & Pareto Evaluator", "goal": "Identificar el frente de Pareto para decisiones multi-objetivo."},
    {"role": "Worst-Case Scenario Planner", "goal": "Modelar escenarios de estrés extremo y planes de contingencia."},
    {"role": "Decision Support Synthesizer", "goal": "Generar matriz de recomendación para la toma de decisiones."}
]

decision_support_crew = create_specialized_crew("Decision Support Crew", "gemini", agents)
