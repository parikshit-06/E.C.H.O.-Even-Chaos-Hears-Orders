"""
media.py
Media / YouTube-related skills for Echo.
"""

from __future__ import annotations

import urllib.parse
import webbrowser


def play_youtube(query: str) -> str:
    """
    Open YouTube search for the given query in the default browser.
    """
    q = query.strip()
    if not q:
        return "What should I play on YouTube?"

    encoded = urllib.parse.quote_plus(q)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    webbrowser.open(url)
    return f"Playing {q} on YouTube (opening results)."
