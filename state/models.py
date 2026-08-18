from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class AnalysisState(BaseModel):
    """
    Estado Pydantic compartido que viaja entre los 20 Crews y 120 Agentes del Flow.
    Garantiza tipado estricto, serialización JSON e integridad de datos.
    """
    raw_data_path: str = ""
    dataframe_json: str = ""
    clean_data_json: str = ""
    
    # Fase 1: Ingesta & Preparación
    data_profile: Dict[str, Any] = Field(default_factory=dict)
    cleaning_report: Dict[str, Any] = Field(default_factory=dict)
    features_added: List[str] = Field(default_factory=list)
    validation_report: Dict[str, Any] = Field(default_factory=dict)
    
    # Fase 2: Definición del Problema
    user_question: str = ""
    problem_type: str = "full_pipeline"
    hypotheses: List[str] = Field(default_factory=list)
    
    # Fase 3: Descriptivo
    descriptive_results: Dict[str, Any] = Field(default_factory=dict)
    
    # Fase 4: Diagnóstico
    diagnostic_results: Dict[str, Any] = Field(default_factory=dict)
    
    # Fase 5: Predictivo
    predictive_results: Dict[str, Any] = Field(default_factory=dict)
    
    # Fase 6: Prescriptivo
    prescriptive_results: Dict[str, Any] = Field(default_factory=dict)
    
    # Fase 7: Reportes & Visualización
    visualizations: List[Dict[str, Any]] = Field(default_factory=list)
    final_report_html: str = ""
    errors: List[str] = Field(default_factory=list)
