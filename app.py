import os
import sys

# Asegurar que el directorio raíz del proyecto esté en sys.path para imports en Streamlit Cloud
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Desactivar telemetría y fijar flags para ChromaDB / CrewAI / LiteLLM
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["LITELLM_DROP_PARAMS"] = "True"
os.environ["LITELLM_DISABLE_PROMPT_CACHING"] = "True"

import litellm
litellm.drop_params = True
litellm.disable_prompt_caching = True

import streamlit as st
import pandas as pd
import json
from dotenv import load_dotenv

# Cargar variables de entorno locales (.env) o secrets de Streamlit Cloud
load_dotenv()
try:
    if hasattr(st, "secrets"):
        for k, v in st.secrets.items():
            if isinstance(v, str) and k not in os.environ:
                os.environ[k] = v
except Exception:
    pass

from flow.analysis_flow import DataAnalysisFlow
from state.models import AnalysisState

st.set_page_config(page_title="🔬 120-Agent CrewAI Data Analyst", layout="wide", page_icon="🔬")

# Custom CSS styling for premium look
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1e293b; margin-bottom: 0.2rem; }
    .sub-caption { font-size: 1rem; color: #64748b; margin-bottom: 1.5rem; }
    .metric-badge { background: #f1f5f9; padding: 4px 10px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🔬 Sistema Multi-Agente CrewAI (120 Agentes)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-caption">Orquestado por CrewAI Flows con 5 LLMs en Rotación (Groq, Cerebras, OpenRouter, Gemini, NVIDIA NIM)</div>', unsafe_allow_html=True)

# Sidebar with provider telemetry
with st.sidebar:
    st.header("⚙️ Configuración & Proveedores")
    st.markdown("""
    **Distribución de 120 Agentes (20 Crews):**
    - ⚡ **Cerebras** (Fase 1 + 7): 36 agentes (10K RPD)
    - 🎯 **OpenRouter / NVIDIA** (Fase 2): 6 agentes (Llama 3.3 70B)
    - 🚀 **Groq** (Fase 3 + 4): 36 agentes (900 RPD)
    - 🧠 **Gemini** (Fase 5 + 6): 42 agentes (1,500 RPD)
    """)
    st.divider()
    flow_mode = st.selectbox("Modo de Enrutamiento", ["Automático (@router inteligente)", "Pipeline Completo (7 Fases)", "Solo Descriptivo & Diagnóstico"])
    st.info("Presupuesto: ~6 ejecuciones completas diarias sin sobrepasar límites gratuitos.")

# File upload section
uploaded_file = st.file_uploader("📁 Carga tu archivo de datos (Excel .xlsx / .xls o CSV)", type=["xlsx", "xls", "csv"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(('xlsx', 'xls')):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        st.success(f"✅ Archivo cargado exitosamente: **{uploaded_file.name}**")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Filas (Registros)", f"{df.shape[0]:,}")
        col2.metric("Columnas (Variables)", f"{df.shape[1]}")
        col3.metric("Valores Nulos", f"{df.isnull().sum().sum():,}")
        col4.metric("Duplicados", f"{df.duplicated().sum():,}")

        st.subheader("👀 Vista Previa del Dataset")
        st.dataframe(df.head(10), use_container_width=True)

        question = st.text_area(
            "🎯 ¿Qué pregunta de negocio o investigación deseas resolver con estos datos?",
            value="Identificar los factores determinantes clave, predecir el comportamiento objetivo y proponer recomendaciones prescriptivas con simulación Monte Carlo.",
            help="Los 120 agentes adaptarán sus hipótesis, modelos predictivos y funciones objetivo a esta pregunta."
        )

        if st.button("🚀 Iniciar Análisis con los 120 Agentes", type="primary", use_container_width=True):
            # Inicializar CrewAI Flow
            flow = DataAnalysisFlow()
            
            # Preparar un payload estructurado y optimizado para LLMs (evita error 413 Request Entity Too Large)
            # Incluye resumen estadístico, tipos de datos, nulos y muestra representativa
            data_summary = {
                "dataset_name": uploaded_file.name,
                "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
                "columns_info": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "null_counts": df.isnull().sum().to_dict(),
                "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {},
                "sample_records": df.head(30).to_dict(orient="records")
            }
            payload_str = json.dumps(data_summary, default=str)
            
            # Asignar propiedades directamente al state existente (CrewAI Flows no permite flow.state = ...)
            flow.state.raw_data_path = uploaded_file.name
            flow.state.dataframe_json = payload_str
            flow.state.clean_data_json = payload_str
            flow.state.user_question = question
            
            if "Solo Descriptivo" in flow_mode:
                flow.state.problem_type = "descriptive_only"
            elif "Pipeline Completo" in flow_mode:
                flow.state.problem_type = "full_pipeline"
            else:
                flow.state.problem_type = "auto"

            phases = [
                ("Fase 1: Ingesta & Data Profiling (Crews 1-4 • Gemini 2.5 Flash)", 0.15),
                ("Fase 2: Definición del Problema & Hipótesis (Crew 5 • Gemini 2.5 Flash)", 0.28),
                ("Fase 3: Análisis Descriptivo & Bivariado (Crews 6-8 • Gemini 2.5 Flash)", 0.45),
                ("Fase 4: Análisis Diagnóstico & Causalidad (Crews 9-11 • Gemini 2.5 Flash)", 0.60),
                ("Fase 5: Modelado Predictivo & Machine Learning (Crews 12-15 • Gemini 2.5 Flash)", 0.78),
                ("Fase 6: Análisis Prescriptivo & Monte Carlo (Crews 16-18 • Gemini 2.5 Flash)", 0.90),
                ("Fase 7: Generación de Reporte Ejecutivo & Visualizaciones (Crews 19-20 • Gemini 2.5 Flash)", 1.00)
            ]

            progress_bar = st.progress(0)
            status_container = st.status("🤖 Orquestando 20 Crews y 120 Agentes...", expanded=True)

            with status_container:
                for phase_name, progress_val in phases:
                    st.write(f"▶️ Ejecutando **{phase_name}**...")
                    progress_bar.progress(progress_val)
                
                # Kickoff CrewAI Flow
                final_result = flow.kickoff()
                status_container.update(label="🎉 ¡Análisis Completo Exitoso!", state="complete", expanded=False)

            st.divider()
            st.subheader("📋 Reporte Final Integrado")
            
            # Obtener el reporte HTML del estado final
            final_report_html = getattr(flow.state, "final_report_html", "") or str(final_result)
            
            if final_report_html:
                st.components.v1.html(final_report_html, height=850, scrolling=True)

            # Download action buttons
            dcol1, dcol2 = st.columns(2)
            with dcol1:
                st.download_button(
                    label="📥 Descargar Reporte HTML Completo",
                    data=final_report_html,
                    file_name="reporte_analisis_crewai_120_agentes.html",
                    mime="text/html",
                    use_container_width=True
                )
            with dcol2:
                clean_df = pd.read_json(flow.state.clean_data_json) if getattr(flow.state, "clean_data_json", None) else df
                st.download_button(
                    label="📥 Descargar Dataset Limpio (CSV)",
                    data=clean_df.to_csv(index=False),
                    file_name="datos_limpios_normalizados.csv",
                    mime="text/csv",
                    use_container_width=True
                )

    except Exception as e:
        st.error(f"Error procesando el archivo: {str(e)}")
else:
    st.info("👆 Por favor sube un archivo CSV o Excel para comenzar el análisis multi-agente.")
