import os
from dotenv import load_dotenv

load_dotenv()

# Per-model API keys (NVIDIA NIM endpoints)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
KIMI_API_KEY = os.getenv("KIMI_API_KEY")

BASE_URL = os.getenv("BASE_URL", "https://integrate.api.nvidia.com/v1/chat/completions")

GEN_MODEL_A = os.getenv("GEN_MODEL_A", "mistralai/mistral-small-4-119b-2603")
GEN_MODEL_B = os.getenv("GEN_MODEL_B", "moonshotai/kimi-k2.5")
VERIFIER_MODEL = os.getenv("VERIFIER_MODEL", "moonshotai/kimi-k2.5")

MAX_TURNS = int(os.getenv("MAX_TURNS", "8"))
GEN_TEMP_A = float(os.getenv("GEN_TEMP_A", "0.4"))
GEN_TEMP_B = float(os.getenv("GEN_TEMP_B", "0.2"))
VERIFIER_TEMP = float(os.getenv("VERIFIER_TEMP", "0.2"))

def get_api_key_for_model(model: str) -> str | None:
    """Return the correct API key based on the model provider."""
    if "mistral" in model.lower():
        return MISTRAL_API_KEY
    elif "kimi" in model.lower() or "moonshot" in model.lower():
        return KIMI_API_KEY
    # Fallback
    return KIMI_API_KEY or MISTRAL_API_KEY
