"""
web_search.py
Opens Google search or direct site.
"""

import webbrowser
import urllib.parse


def search_web(query: str) -> str:
    q = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={q}"
    webbrowser.open(url)
    return f"Searching the web for {query}"
