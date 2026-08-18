from crewai import Agent, Task, Crew, Process
from utils.llm_router import get_llm
from typing import List, Dict, Any

def create_specialized_crew(
    crew_name: str,
    provider: str,
    agents_spec: List[Dict[str, Any]],
    tasks_spec: List[Dict[str, Any]] = None
) -> Crew:
    """
    Construye una Crew con 6 agentes hiper-especializados, tareas encadenadas y asignación de LLM.
    """
    llm = get_llm(provider)
    agents = []
    
    for spec in agents_spec:
        agent = Agent(
            role=spec["role"],
            goal=spec["goal"],
            backstory=spec.get("backstory", f"Experto senior con más de 12 años en {spec['role']}."),
            llm=llm,
            tools=spec.get("tools", []),
            max_iter=3,
            max_rpm=15,
            verbose=False,
            allow_delegation=False
        )
        agents.append(agent)
    
    tasks = []
    if tasks_spec:
        for i, tspec in enumerate(tasks_spec):
            assigned_agent = agents[tspec.get("agent_idx", min(i, len(agents) - 1))]
            task = Task(
                description=tspec["description"],
                agent=assigned_agent,
                expected_output=tspec.get("expected_output", "Resultado analítico en formato estructurado o JSON.")
            )
            tasks.append(task)
    else:
        # Tareas autogeneradas para cada uno de los agentes con límite seguro de contexto
        for i, agent in enumerate(agents):
            task = Task(
                description=f"Ejecutar análisis experto de {agent.role} considerando el objetivo: {agent.goal}. Datos e información del dataset: {{data}}",
                agent=agent,
                expected_output=f"Informe sintético, cuantitativo y diagnóstico detallado por {agent.role}."
            )
            tasks.append(task)

    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=False,
        max_rpm=20
    )
