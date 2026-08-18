from crewai.tools import tool
import numpy as np
from scipy.optimize import linprog
import json

@tool
def solve_linear_program(c_json: str, A_ub_json: str, b_ub_json: str) -> str:
    """Resuelve un problema de optimización lineal: min c^T * x tal que A_ub * x <= b_ub"""
    c = json.loads(c_json)
    A_ub = json.loads(A_ub_json)
    b_ub = json.loads(b_ub_json)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, method='highs')
    return json.dumps({
        "success": bool(res.success),
        "optimal_value": float(res.fun),
        "optimal_solution": [float(x) for x in res.x]
    })

@tool
def run_monte_carlo_simulation(base_value: float, std_pct: float = 0.15, iterations: int = 10000) -> str:
    """Simula 10,000 iteraciones estocásticas con distribución normal truncada"""
    samples = np.random.normal(loc=base_value, scale=base_value * std_pct, size=iterations)
    return json.dumps({
        "iterations": iterations,
        "mean": float(np.mean(samples)),
        "std": float(np.std(samples)),
        "p10": float(np.percentile(samples, 10)),
        "p50": float(np.percentile(samples, 50)),
        "p90": float(np.percentile(samples, 90)),
        "prob_positive": float(np.mean(samples > base_value))
    })
