"""
memory.py
Structured memory storage + retrieval for Echo.
"""

from __future__ import annotations
import os, json
from datetime import datetime
from typing import List, Dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_PATH = os.path.join(DATA_DIR, "memory.json")


def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_memory() -> List[Dict]:
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_memory(mem: List[Dict]):
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)


def store_memory(text: str) -> str:
    _ensure_dir()
    mem = _load_memory()

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "fact": text.strip(),
        "tags": text.lower().split(),  # basic tagging for now
    }

    mem.append(entry)
    _save_memory(mem)
    return "Okay, I'll remember that."


def recall_memory(query: str) -> str:
    mem = _load_memory()
    if not mem:
        return "I don't remember anything yet."

    q = query.lower()
    matches = [m for m in mem if q in m["fact"].lower() or q in m["tags"]]

    if not matches:
        return f"I don't remember anything about {query}."

    # SUMMARIZE matched facts using LLM later
    facts = "; ".join(m['fact'] for m in matches)
    return f"Here's what I remember about {query}: {facts}"
