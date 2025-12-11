import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    assistant_name: str = "Echo"
    language: str = "en"

    stt_backend: str = "whisper_local"
    tts_backend: str = "pyttsx3"
    llm_backend: str = os.getenv("LLM_BACKEND", "perplexity")
    response_mode: str = os.getenv("RESPONSE_MODE", "voice")

    # API keys
    perplexity_api_key: str = os.getenv("PERPLEXITY_API_KEY", "")
    perplexity_model: str = os.getenv("PERPLEXITY_MODEL", "sonar-reasoning")

    # Hotkey / wake-word
    hotkey: str = "ctrl+space"
    porcupine_access_key: str = os.getenv("PORCUPINE_ACCESS_KEY", "")
    wakeword_keyword: str = os.getenv("WAKEWORD_KEYWORD", "hey jarvis")  # openWakeWord model name

    # Audio / STT
    sample_rate: int = 16_000
    audio_channels: int = 1
    stt_model_name: str = "small"
    stt_device: str = "cpu"
    stt_compute_type: str = "int8"


def load_config() -> Config:
    return Config()
