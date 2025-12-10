"""
brain.py
LLM / "brain" interface for Echo Assistant.

Right now this is a simple rule-based / echo brain.
Later we'll add real backends (OpenAI, Ollama, etc.) behind the same API.
"""

from __future__ import annotations
import os
from dataclasses import dataclass
from typing import List, Literal, Optional, Tuple


@dataclass
class BrainConfig:
    backend: str = "dummy"  # "dummy", "openai", "ollama", gemini, perplexity, etc. later
    assistant_name: str = "E.C.H.O."


MessageRole = Literal["system", "user", "assistant"]


@dataclass
class Message:
    role: MessageRole
    content: str


class Brain:
    def __init__(self, config: Optional[BrainConfig] = None) -> None:
        self.config = config or BrainConfig()
        self.history: List[Message] = []

        # simple system prompt for future LLMs
        self.system_prompt = (
            f"You are {self.config.assistant_name}, a desktop voice assistant. "
            "You respond concisely and helpfully."
        )
        self.history.append(Message(role="system", content=self.system_prompt))

    # Public API
    def generate_reply(self, user_text: str) -> str:
        user_text = user_text.strip()
        if not user_text:
            return "I didn't hear anything."

        try:
            if self.config.backend == "dummy":
                reply = self._dummy_backend(user_text)
            elif self.config.backend == "gemini":
                reply = self._gemini_backend(user_text)
            elif self.config.backend == "perplexity":
                reply = self._perplexity_backend(user_text)
            elif self.config.backend == "openai":
                reply = self._openai_backend(user_text)
            elif self.config.backend == "ollama":
                reply = self._ollama_backend(user_text)
            else:
                reply = f"Backend '{self.config.backend}' is not implemented yet."
        except Exception as e:
            reply = f"There was an error talking to the {self.config.backend} backend: {e}"

        self.history.append(Message(role="user", content=user_text))
        self.history.append(Message(role="assistant", content=reply))
        self._trim_history(max_messages=15)
        return reply

    # ---- Backends ----

    def _dummy_backend(self, user_text: str) -> str:
        """
        Very simple canned logic so we can build everything else
        before plugging in a real LLM.
        """
        text = user_text.strip()
        lower = text.lower()
        name = self.config.assistant_name

        if not text:
            return "I didn't hear anything."

        if "your name" in lower:
            return f"My name is {name}."

        if "what can you do" in lower or "who are you" in lower:
            return (
                f"I'm {name}, your local voice assistant. "
                "Right now I can listen, transcribe, and talk back. "
                "We'll add app control and smarter reasoning soon."
            )

        if "time" in lower and "what" in lower:
            # We deliberately keep it simple for now, no timezone mental math.
            import datetime
            now = datetime.datetime.now().strftime("%H:%M")
            return f"It is currently {now}."

        # fallback: simple echo with a bit of attitude
        return f"You said: {text}. I'm still a dummy brain; we'll upgrade me soon."
    
    def _gemini_backend(self, user_text: str) -> str:
        import google.generativeai as genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Gemini API key is missing. Set GEMINI_API_KEY in your .env."

        genai.configure(api_key=api_key)

        # Use the exact model name from GEMINI_MODEL (e.g. 'models/gemini-pro')
        model_name = os.getenv("GEMINI_MODEL")
        if not model_name:
            return "GEMINI_MODEL is not set. Use debug_gemini_models.py to pick one."

        try:
            print(f"[Gemini] Using model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(user_text)
        except Exception as e:
            return f"Gemini backend error: {e}"

        text = getattr(response, "text", None)
        if not text:
            return "Gemini returned an empty response."
        return text.strip()

    
    def _perplexity_backend(self, user_text: str) -> str:
        import requests, json

        api_key = os.getenv("PERPLEXITY_API_KEY")
        model = os.getenv("PERPLEXITY_MODEL", "sonar-reasoning")

        if not api_key:
            return "Perplexity API key is missing. Set PERPLEXITY_API_KEY in your .env."

        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_text},
            ],
            # these fields are accepted by their OpenAI-compatible API
            "max_tokens": 500,
            "temperature": 0.7,
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
        except Exception as e:
            return f"Perplexity request error (network): {e}"

        # If status is not 2xx, show the error body so we actually see what's wrong
        if not resp.ok:
            try:
                err_json = resp.json()
            except Exception:
                err_json = resp.text
            return f"Perplexity API error {resp.status_code}: {err_json}"

        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return f"Unexpected Perplexity response format: {data}"

    
    def _openai_backend(self, user_text: str) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Build messages from history
        msgs = [{"role": m.role, "content": m.content} for m in self.history]
        msgs.append({"role": "user", "content": user_text})

        response = client.chat.completions.create(
            model="gpt-4.1-mini",   # or any model you prefer
            messages=msgs,
            temperature=0.7,
        )
        return response.choices[0].message.content
    
    def _ollama_backend(self, user_text: str) -> str:
        import requests, json
        model = os.getenv("OLLAMA_MODEL","llama3.2")

        payload = {
            "model": model,
            "messages": [
                {"role": m.role, "content": m.content} for m in self.history
            ] + [{"role": "user", "content": user_text}],
            "stream": False
        }

        r = requests.post("http://localhost:11434/api/chat", json=payload)
        data = r.json()
        return data["message"]["content"]


    # ---- History mgmt ----

    def _trim_history(self, max_messages: int) -> None:
        """
        Keep history from growing indefinitely. Always keep the system prompt.
        """
        if len(self.history) <= max_messages:
            return
        # keep first (system) + last N-1 messages
        system = self.history[0]
        tail = self.history[-(max_messages - 1):]
        self.history = [system] + tail
