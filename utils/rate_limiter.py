import time
from threading import Lock
from collections import defaultdict

class MultiProviderRateLimiter:
    """
    Controlador de Rate Limits thread-safe para los providers gratuitos (2026 Free Tier).
    Garantiza márgenes de seguridad para evitar errores 429 (Too Many Requests).
    """
    LIMITS = {
        "groq": {"rpm": 25, "rpd": 900},          # 30 RPM nominal
        "cerebras": {"rpm": 25, "rpd": 10000},     # 30 RPM nominal, 1M TPD
        "gemini": {"rpm": 12, "rpd": 1300},        # 15 RPM nominal
        "openrouter": {"rpm": 20, "rpd": 5000},    # Según cuota de OpenRouter
        "nvidia": {"rpm": 20, "rpd": 5000},        # 1000 créditos free
        "sambanova": {"rpm": 15, "rpd": 5000},     # 20 RPM nominal
    }
    
    def __init__(self):
        self.minute_requests = defaultdict(list)
        self.daily_requests = defaultdict(list)
        self.lock = Lock()
    
    def wait_if_needed(self, provider: str):
        with self.lock:
            now = time.time()
            limits = self.LIMITS.get(provider, {"rpm": 10, "rpd": 1000})
            
            # Limpiar marcas de tiempo antiguas
            self.minute_requests[provider] = [t for t in self.minute_requests[provider] if now - t < 60]
            self.daily_requests[provider] = [t for t in self.daily_requests[provider] if now - t < 86400]
            
            # Verificar RPM (Requests por Minuto)
            if len(self.minute_requests[provider]) >= limits["rpm"]:
                sleep_time = 60 - (now - self.minute_requests[provider][0])
                time.sleep(max(0.1, sleep_time))
            
            # Verificar RPD (Requests por Día)
            if len(self.daily_requests[provider]) >= limits["rpd"]:
                raise Exception(f"{provider} daily limit reached, switching to fallback provider")
            
            self.minute_requests[provider].append(time.time())
            self.daily_requests[provider].append(time.time())

rate_limiter = MultiProviderRateLimiter()
