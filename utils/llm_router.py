import os
import litellm
from crewai import LLM
from utils.rate_limiter import rate_limiter

# Configuración global para descartar parámetros incompatibles
litellm.drop_params = True
litellm.disable_prompt_caching = True

_llm_cache = {}

def _create_llm_instance(provider: str):
    """
    Inicialización de LLMs robusta con Google Gemini y NVIDIA NIM (Llama 3.3 70B).
    """
    gemini_key = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    nvidia_key = os.getenv("NVIDIA_API_KEY", "")
    
    # 1. NVIDIA NIM (Llama 3.3 70B Instruct en endpoints OpenAI-compatibles)
    if provider == "nvidia":
        return LLM(
            model="openai/meta/llama-3.3-70b-instruct",
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=nvidia_key,
            temperature=0.1,
            max_tokens=4096
        )

    # 2. Google Gemini 1.5 Flash (Backup con cuota independiente)
    elif provider == "gemini_15":
        return LLM(
            model="gemini/gemini-1.5-flash",
            api_key=gemini_key,
            temperature=0.1,
            max_tokens=4096
        )

    # 3. Google Gemini 1.5 Pro
    elif provider == "gemini_pro":
        return LLM(
            model="gemini/gemini-1.5-pro",
            api_key=gemini_key,
            temperature=0.1,
            max_tokens=4096
        )

    # 4. Google Gemini 2.5 Flash (Motor primario de alta velocidad)
    elif provider in ["gemini", "gemini_flash"]:
        return LLM(
            model="gemini/gemini-2.5-flash",
            api_key=gemini_key,
            temperature=0.1,
            max_tokens=4096
        )

    # Fallback default: Si existe NVIDIA API key y no Gemini, usar NVIDIA; de lo contrario Gemini
    if nvidia_key and not gemini_key:
        return LLM(
            model="openai/meta/llama-3.3-70b-instruct",
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=nvidia_key,
            temperature=0.1,
            max_tokens=4096
        )

    return LLM(
        model="gemini/gemini-2.5-flash",
        api_key=gemini_key,
        temperature=0.1,
        max_tokens=4096
    )

# Cadena de Fallback integral activa entre Gemini y NVIDIA NIM
FALLBACK_CHAIN = {
    "gemini": ["nvidia", "gemini_15", "gemini_pro"],
    "nvidia": ["gemini", "gemini_15", "gemini_pro"],
    "gemini_15": ["nvidia", "gemini", "gemini_pro"],
    "gemini_pro": ["nvidia", "gemini", "gemini_15"],
}

# Mapeo metodológico balanceado entre Gemini y NVIDIA NIM
LLM_ROUTING = {
    "phase1": "gemini",        # Ingesta & Data Profiling (Gemini 2.5 Flash)
    "phase2": "nvidia",        # Definición de Hipótesis & Target Scoping (NVIDIA NIM Llama 3.3 70B)
    "phase3": "gemini",        # Análisis Descriptivo & Bivariado (Gemini 2.5 Flash)
    "phase4": "nvidia",        # Diagnóstico Econométrico & Causal (NVIDIA NIM Llama 3.3 70B)
    "phase5": "gemini",        # Modelado Predictivo & Machine Learning (Gemini 2.5 Flash)
    "phase6": "gemini",        # Optimización Prescriptiva & Monte Carlo (Gemini 2.5 Flash)
    "phase7": "nvidia",        # Ensamblaje y Generación de Reportes (NVIDIA NIM Llama 3.3 70B)
}

def get_llm(primary: str = "gemini"):
    """
    Retorna la instancia de LLM aplicando rate-limiting y fallback automático
    entre Google Gemini y NVIDIA NIM (Llama 3.3 70B).
    """
    if primary not in ["gemini", "nvidia", "gemini_15", "gemini_pro"]:
        primary = "gemini"

    providers = [primary] + FALLBACK_CHAIN.get(primary, ["nvidia", "gemini_15"])
    for provider in providers:
        try:
            rate_limiter.wait_if_needed(provider)
            if provider not in _llm_cache:
                _llm_cache[provider] = _create_llm_instance(provider)
            return _llm_cache[provider]
        except Exception:
            continue
            
    # Instancia de emergencia
    if primary not in _llm_cache:
        _llm_cache[primary] = _create_llm_instance(primary)
    return _llm_cache[primary]
