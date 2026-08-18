from crewai.tools import tool
import pandas as pd
import numpy as np
from scipy import stats
import json

@tool
def calculate_correlations(data_json: str) -> str:
    """Calcula matrices de correlación Pearson y Spearman con p-valores"""
    df = pd.read_json(data_json).select_dtypes(include='number')
    corr_matrix = df.corr(method='pearson').to_dict()
    return json.dumps(corr_matrix)

@tool
def run_ttest_anova(data_json: str, group_col: str, val_col: str) -> str:
    """Ejecuta t-test de 2 grupos o ANOVA de múltiples grupos con significancia"""
    df = pd.read_json(data_json)
    groups = [group[val_col].dropna().values for _, group in df.groupby(group_col)]
    if len(groups) == 2:
        stat, pval = stats.ttest_ind(groups[0], groups[1])
        return json.dumps({"test": "t-test", "statistic": float(stat), "p_value": float(pval)})
    elif len(groups) > 2:
        stat, pval = stats.f_oneway(*groups)
        return json.dumps({"test": "ANOVA", "statistic": float(stat), "p_value": float(pval)})
    return json.dumps({"error": "Insufficient groups"})

@tool
def calculate_cohens_d(data_json: str, group_col: str, val_col: str) -> str:
    """Calcula tamaño del efecto d de Cohen entre 2 grupos"""
    df = pd.read_json(data_json)
    groups = [group[val_col].dropna().values for _, group in df.groupby(group_col)]
    if len(groups) >= 2:
        n1, n2 = len(groups[0]), len(groups[1])
        s1, s2 = np.var(groups[0], ddof=1), np.var(groups[1], ddof=1)
        pooled_se = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
        d = (np.mean(groups[0]) - np.mean(groups[1])) / pooled_se
        return json.dumps({"cohens_d": float(d), "magnitude": "large" if abs(d) > 0.8 else "medium" if abs(d) > 0.5 else "small"})
    return json.dumps({"error": "Need 2 groups"})
