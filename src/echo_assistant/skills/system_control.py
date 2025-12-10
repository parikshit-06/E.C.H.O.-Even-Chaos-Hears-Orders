"""
system_control.py
Basic OS-level commands.
"""

import subprocess
import os
import webbrowser

APPS = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vs code": "code",
    "vscode": "code",
    "notepad": "notepad.exe",
    "explorer": "explorer.exe",
    "calculator": "calc.exe",
    "terminal": "wt.exe",
    "cmd": "cmd.exe",
    "spotify": "spotify",
    "firefox": "firefox",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "paint": "mspaint",
    "camera": "microsoft.windows.camera:",
    "settings": "ms-settings:",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "stackoverflow": "https://stackoverflow.com",
    "reddit": "https://www.reddit.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "amazon": "https://www.amazon.com",
    "netflix": "https://www.netflix.com",
    "news": "https://news.google.com",
    "weather": "https://www.weather.com",
    "maps": "https://www.google.com/maps",
    "calendar": "https://calendar.google.com",
    "drive": "https://drive.google.com",
    "docs": "https://docs.google.com",
    "sheets": "https://sheets.google.com",
    "slides": "https://slides.google.com",
    "translate": "https://translate.google.com",
    "photos": "https://photos.google.com",
    "youtube music": "https://music.youtube.com",
}

def open_app(app_name: str) -> str:
    app_name = app_name.lower()

    # best match
    for key, cmd in APPS.items():
        if key in app_name:
            try:
                subprocess.Popen(cmd)
                return f"Opening {key}"
            except FileNotFoundError:
                return f"{key} not found or not in PATH."

    return f"I don't know how to open {app_name} yet."
