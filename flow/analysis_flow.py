from crewai.flow.flow import Flow, listen, start, router
from state.models import AnalysisState

# Import Crews de las 7 Fases
from crews.phase1_ingestion.data_profiling_crew import data_profiling_crew
from crews.phase1_ingestion.data_cleaning_crew import data_cleaning_crew
from crews.phase1_ingestion.feature_engineering_crew import feature_engineering_crew
from crews.phase1_ingestion.data_validation_crew import data_validation_crew

from crews.phase2_definition.problem_definition_crew import problem_definition_crew

from crews.phase3_descriptive.univariate_crew import univariate_crew
from crews.phase3_descriptive.bivariate_crew import bivariate_crew
from crews.phase3_descriptive.temporal_crew import temporal_crew

from crews.phase4_diagnostic.correlation_crew import correlation_crew
from crews.phase4_diagnostic.regression_diagnostics_crew import regression_diagnostics_crew
from crews.phase4_diagnostic.factor_analysis_crew import factor_analysis_crew

from crews.phase5_predictive.classification_crew import classification_crew
from crews.phase5_predictive.regression_models_crew import regression_models_crew
from crews.phase5_predictive.forecasting_crew import forecasting_crew
from crews.phase5_predictive.clustering_crew import clustering_crew

from crews.phase6_prescriptive.optimization_crew import optimization_crew
from crews.phase6_prescriptive.decision_support_crew import decision_support_crew
from crews.phase6_prescriptive.strategy_crew import strategy_crew

from crews.phase7_reporting.visualization_crew import visualization_crew
from crews.phase7_reporting.report_generation_crew import report_generation_crew


class DataAnalysisFlow(Flow[AnalysisState]):
    """
    CrewAI Flow maestro que orquesta los 120 agentes distribuidos en 20 Crews y 7 Fases.
    Utiliza @router para evitar llamadas innecesarias a LLMs y optimizar el rate-limiting.
    """

    @start()
    def ingest_and_prepare(self):
        """FASE 1: Ingesta, Profiling, Limpieza, Feature Engineering y Validación (Cerebras)"""
        # Crew 1: Data Profiling
        profile_res = data_profiling_crew.kickoff(inputs={"data": self.state.dataframe_json})
        self.state.data_profile = getattr(profile_res, 'pydantic', {}).dict() if hasattr(getattr(profile_res, 'pydantic', None), 'dict') else {}

        # Crew 2: Data Cleaning
        cleaned_res = data_cleaning_crew.kickoff(inputs={
            "data": self.state.dataframe_json,
            "profile": str(self.state.data_profile)
        })
        self.state.clean_data_json = getattr(getattr(cleaned_res, 'pydantic', None), 'clean_data', self.state.dataframe_json)
        self.state.cleaning_report = getattr(getattr(cleaned_res, 'pydantic', None), 'report', {})

        # Crew 3: Feature Engineering
        featured_res = feature_engineering_crew.kickoff(inputs={"data": self.state.clean_data_json})
        self.state.features_added = getattr(getattr(featured_res, 'pydantic', None), 'features', [])

        # Crew 4: Data Validation
        validated_res = data_validation_crew.kickoff(inputs={"data": self.state.clean_data_json})
        self.state.validation_report = getattr(validated_res, 'pydantic', {}).dict() if hasattr(getattr(validated_res, 'pydantic', None), 'dict') else {}
        return "prepared"

    @listen(ingest_and_prepare)
    def define_problem(self):
        """FASE 2: Crew 5 - Definición del Problema, Clasificación de Target e Hipótesis (OpenRouter)"""
        result = problem_definition_crew.kickoff(inputs={
            "data": self.state.clean_data_json,
            "data_profile": str(self.state.data_profile),
            "user_question": self.state.user_question
        })
        if hasattr(result, 'pydantic') and result.pydantic:
            self.state.problem_type = getattr(result.pydantic, 'problem_type', 'full_pipeline')
            self.state.hypotheses = getattr(result.pydantic, 'hypotheses', [])
        else:
            self.state.problem_type = "full_pipeline"
            self.state.hypotheses = ["H1: Las variables independientes explican significativamente la varianza."]
        return result

    @router(define_problem)
    def route_analysis(self):
        """Enrutador dinámico que decide qué fases ejecutar según el tipo de problema detectado"""
        if self.state.problem_type == "descriptive_only":
            return "descriptive_branch"
        elif self.state.problem_type == "diagnostic":
            return "through_diagnostic"
        else:
            return "full_pipeline"

    @listen(route_analysis)
    def run_descriptive(self):
        """FASE 3: Crews 6-8 - Análisis Univariado, Bivariado y Temporal (Groq)"""
        uni = univariate_crew.kickoff(inputs={"data": self.state.clean_data_json})
        biv = bivariate_crew.kickoff(inputs={"data": self.state.clean_data_json})
        temp = temporal_crew.kickoff(inputs={"data": self.state.clean_data_json})

        self.state.descriptive_results = {
            "univariate": str(uni),
            "bivariate": str(biv),
            "temporal": str(temp)
        }
        return "descriptive_done"

    @router(run_descriptive)
    def check_diagnostic(self):
        if self.state.problem_type == "descriptive_only":
            return "skip_to_report"
        return "run_diagnostic"

    @listen(check_diagnostic)
    def run_diagnostic(self):
        """FASE 4: Crews 9-11 - Causalidad, Regresión y Diagnóstico Factorial (Groq)"""
        if self.state.problem_type == "descriptive_only":
            return "skipped"

        corr = correlation_crew.kickoff(inputs={"data": self.state.clean_data_json})
        reg = regression_diagnostics_crew.kickoff(inputs={"data": self.state.clean_data_json})
        factor = factor_analysis_crew.kickoff(inputs={"data": self.state.clean_data_json})

        self.state.diagnostic_results = {
            "correlations": str(corr),
            "regressions": str(reg),
            "factors": str(factor)
        }
        return "diagnostic_done"

    @router(run_diagnostic)
    def check_predictive(self):
        if self.state.problem_type in ["descriptive_only", "diagnostic"]:
            return "skip_to_report"
        return "run_predictive"

    @listen(check_predictive)
    def run_predictive(self):
        """FASE 5: Crews 12-15 - Modelado Predictivo, Forecasting y Segmentación (Gemini)"""
        if self.state.problem_type in ["descriptive_only", "diagnostic"]:
            return "skipped"

        if self.state.problem_type == "classification":
            pred = classification_crew.kickoff(inputs={"data": self.state.clean_data_json})
        elif self.state.problem_type == "regression":
            pred = regression_models_crew.kickoff(inputs={"data": self.state.clean_data_json})
        elif self.state.problem_type == "forecasting":
            pred = forecasting_crew.kickoff(inputs={"data": self.state.clean_data_json})
        elif self.state.problem_type == "segmentation":
            pred = clustering_crew.kickoff(inputs={"data": self.state.clean_data_json})
        else:
            pred = classification_crew.kickoff(inputs={"data": self.state.clean_data_json})
            clustering_crew.kickoff(inputs={"data": self.state.clean_data_json})

        self.state.predictive_results = {"model_evaluation": str(pred)}
        return "predictive_done"

    @listen(run_predictive)
    def run_prescriptive(self):
        """FASE 6: Crews 16-18 - Optimización Lineal, Monte Carlo y Recomendaciones (Gemini)"""
        if self.state.problem_type in ["descriptive_only", "diagnostic"]:
            return "skipped"

        opt = optimization_crew.kickoff(inputs={"data": self.state.clean_data_json})
        dec = decision_support_crew.kickoff(inputs={"data": self.state.clean_data_json})
        strat = strategy_crew.kickoff(inputs={"data": self.state.clean_data_json})

        self.state.prescriptive_results = {
            "optimization": str(opt),
            "decisions": str(dec),
            "strategy": str(strat)
        }
        return "prescriptive_done"

    @listen(run_prescriptive)
    def generate_report(self):
        """FASE 7: Crews 19-20 - Visualización y Ensamblaje del Reporte HTML (Cerebras)"""
        viz = visualization_crew.kickoff(inputs={"data": self.state.clean_data_json})
        report = report_generation_crew.kickoff(inputs={
            "data": self.state.clean_data_json,
            "descriptive": str(self.state.descriptive_results),
            "diagnostic": str(self.state.diagnostic_results),
            "predictive": str(self.state.predictive_results),
            "prescriptive": str(self.state.prescriptive_results),
            "visualizations": str(viz)
        })
        self.state.final_report_html = str(report)
        return self.state
