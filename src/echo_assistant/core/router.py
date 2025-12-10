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
from ..skills.notes import add_note, list_notes, search_notes
from ..skills.media import play_youtube
from ..skills.memory import store_memory, recall_memory


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

        # --- Skill: Notes ---

        # Add notes
        if lower.startswith(("take a note", "create a note", "note that", "remember that")):
            for phrase in ["take a note", "create a note", "note that", "remember that"]:
                if lower.startswith(phrase):
                    content = text[len(phrase):].strip(" :")
                    return RouteResult(kind="control", reply=add_note(content or "Empty note."))

        # Show notes
        if any(p in lower for p in [
            "show my notes", "show me my notes", "read my notes",
            "list my notes", "display my notes", "open my notes"
        ]):
            return RouteResult(kind="control", reply=list_notes(limit=5))

        # Search notes
        if lower.startswith("search my notes for"):
            query = text.replace("search my notes for", "", 1).strip(" :")
            return RouteResult(kind="control", reply=search_notes(query))

        if lower.startswith("find notes about"):
            query = text.replace("find notes about", "", 1).strip(" :")
            return RouteResult(kind="control", reply=search_notes(query))
        
        # --- Skill: Play on YouTube ---
        if lower.startswith("play "):
            # strip leading "play "
            content = text[5:].strip()

            # remove trailing "on youtube"/"on you tube"/"from youtube"/"on yt"
            endings = [
                "on youtube",
                "on you tube",
                "from youtube",
                "on yt",
            ]
            clower = content.lower()
            for ending in endings:
                if clower.endswith(ending):
                    content = content[: -len(ending)].strip(" ,.")
                    break

            return RouteResult(kind="control", reply=play_youtube(content))
        
        # --- Skill: Memory Store ---
        if lower.startswith(("remember that", "remember to", "remember")):
            content = text.replace("remember that", "", 1)\
                        .replace("remember to", "", 1)\
                        .replace("remember", "", 1).strip(" :")
            return RouteResult(kind="control", reply=store_memory(content or "Blank memory."))

        # --- Skill: Memory Recall ---
        if lower.startswith(("what do you remember about", "what do you know about", "recall")):
            content = text.replace("what do you remember about", "", 1)\
                        .replace("what do you know about", "", 1)\
                        .replace("recall", "", 1).strip(" :")
            return RouteResult(kind="control", reply=recall_memory(content))

        # fallback -> LLM brain
        reply = self.brain.generate_reply(text)
        return RouteResult(kind="chat", reply=reply, should_exit=False)

