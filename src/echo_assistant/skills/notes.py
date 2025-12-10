"""
notes.py
Simple note-taking skill for Echo.

Features:
- Add a note
- List recent notes
- Search notes by keyword
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import List

# store notes in project root / data dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
NOTES_PATH = os.path.join(DATA_DIR, "notes.txt")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def add_note(text: str) -> str:
    """
    Append a note with timestamp to notes.txt
    """
    _ensure_data_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"[{timestamp}] {text.strip()}\n"

    with open(NOTES_PATH, "a", encoding="utf-8") as f:
        f.write(line)

    return "Note saved."


def _load_notes() -> List[str]:
    if not os.path.exists(NOTES_PATH):
        return []
    with open(NOTES_PATH, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def list_notes(limit: int = 5) -> str:
    """
    Return the most recent `limit` notes as a single string.
    """
    notes = _load_notes()
    if not notes:
        return "You have no notes yet."

    last_notes = notes[-limit:]
    # Don't let TTS read 10 paragraphs at once
    joined = " | ".join(last_notes)
    return f"Your last {len(last_notes)} notes are: {joined}"


def search_notes(query: str, limit: int = 5) -> str:
    """
    Search notes containing the query (case-insensitive).
    """
    q = query.strip().lower()
    if not q:
        return "What should I search for in your notes?"

    notes = _load_notes()
    if not notes:
        return "You have no notes yet."

    matches = [n for n in notes if q in n.lower()]
    if not matches:
        return f"I couldn't find any notes containing '{query}'."

    top = matches[-limit:]
    joined = " | ".join(top)
    return f"I found {len(matches)} notes matching '{query}'. Here are some: {joined}"
