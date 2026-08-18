# 🔬 Sistema Multi-Agente CrewAI de Análisis de Datos (120 Agentes)

Sistema integral de analítica de datos impulsado por **CrewAI Flows**, compuesto por **120 agentes especializados organizados en 20 Crews de 6 agentes cada una**, distribuidas en 7 fases metodológicas impulsadas por **Google Gemini 2.5 Flash** y **NVIDIA NIM (Llama 3.3 70B)** con malla de fallback automático.

## 🚀 Despliegue en Streamlit Cloud (1-Click)

### ⚠️ Versión de Python:
CrewAI y ChromaDB requieren **Python 3.11** o **Python 3.12**. El proyecto incluye `.python-version` y `runtime.txt` configurados en **`3.11`**.

1. **Crear Repositorio en GitHub:**
   - Descarga este proyecto y súbelo a tu repositorio en GitHub.
2. **Conectar en Streamlit Community Cloud:**
   - Ingresa a [share.streamlit.io](https://share.streamlit.io)
   - Selecciona **New app**, elige tu repositorio y el archivo principal `app.py`.
3. **Configurar Secrets (Gemini + NVIDIA NIM):**
   - En la configuración de tu app en Streamlit (**Settings > Secrets**), pega tus claves:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   GOOGLE_API_KEY = "AIzaSy..."
   NVIDIA_API_KEY = "nvapi-..."
   ```
4. **¡Listo!** El sistema analizará cualquier dataset de principio a fin con máxima estabilidad.
