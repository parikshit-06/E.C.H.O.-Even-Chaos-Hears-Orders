"""
router.py
Decides how to handle user text:
- special control phrases (exit, stop)
- future: skills (open app, search, notes)
- fallback: chat via Brain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from .brain import Brain, BrainConfig

from ..skills.system_control import open_app
from ..skills.web_search import search_web
from ..skills.notes import add_note, list_notes, search_notesS

RouteType = Literal["control", "chat"]


@dataclass
class RouteResult:
    kind: RouteType
    reply: str
    should_exit: bool = False


class Router:
    def __init__(self, brain: Optional[Brain] = None) -> None:
        self.brain = brain or Brain(BrainConfig())

    def route(self, user_text: str) -> RouteResult:
        text = user_text.strip()
        lower = text.lower()

        # --- Exit Commands ---
        if any(phrase in lower for phrase in ["exit assistant", "stop assistant", "quit assistant"]):
            return RouteResult(kind="control", reply="Shutting down.", should_exit=True)

        # --- Skill: Open App ---
        if lower.startswith("open "):
            app = lower.replace("open", "", 1).strip()
            return RouteResult(kind="control", reply=open_app(app))

        # --- Skill: Web Search ---
        if lower.startswith("search for "):
            query = lower.replace("search for", "", 1).strip()
            return RouteResult(kind="control", reply=search_web(query))

        if lower.startswith("search "):
            query = lower.replace("search", "", 1).strip()
            return RouteResult(kind="control", reply=search_web(query))

        # fallback -> LLM brain
        reply = self.brain.generate_reply(text)
        return RouteResult(kind="chat", reply=reply, should_exit=False)

