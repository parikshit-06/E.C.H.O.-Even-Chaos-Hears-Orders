import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


@dataclass
class Config:
    # Core assistant identity
    assistant_name: str = "Echo"
    language: str = "en"

    # Backends
    stt_backend: str = "whisper_local"    # currently unused, but reserved
    tts_backend: str = "pyttsx3"
    llm_backend: str = os.getenv("LLM_BACKEND", "dummy")  # "dummy", "gemini", "perplexity", etc.

    # API keys (optional depending on backend)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    perplexity_api_key: str = os.getenv("PERPLEXITY_API_KEY", "")
    perplexity_model: str = os.getenv("PERPLEXITY_MODEL", "sonar-reasoning")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")

    # Hotkey config (for later)
    hotkey: str = "ctrl+space"

    # Audio config
    sample_rate: int = 16_000
    audio_channels: int = 1

    # STT-specific config
    stt_model_name: str = "small"
    stt_device: str = "cpu"
    stt_compute_type: str = "int8"


def load_config() -> Config:
    """
    Factory function to create a Config object.
    Keeps a single obvious entrypoint for all other modules.
    """
    return Config()
