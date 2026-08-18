from crews.crew_factory import create_specialized_crew

agents = [
    {"role": "Objective Function Formulator", "goal": "Definir función objetivo (maximizar beneficio o minimizar costo)."},
    {"role": "Constraint Architect", "goal": "Modelar restricciones de capacidad, presupuesto y cotas de variables."},
    {"role": "Linear Program Solver", "goal": "Resolver mediante Simplex / HiGHS y verificar optimalidad."},
    {"role": "Sensitivity & Shadow Price Analyst", "goal": "Calcular precios sombra y holgura de cada restricción."},
    {"role": "Integer & Mixed Program Specialist", "goal": "Evaluar variables de decisión binarias y discretas."},
    {"role": "Optimization Solution Synthesizer", "goal": "Traducir los vectores de solución en acciones concretas."}
]

optimization_crew = create_specialized_crew("Optimization Crew", "gemini", agents)
