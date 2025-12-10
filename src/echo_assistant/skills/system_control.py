"""
system_control.py
Basic OS-level commands + website launch for Echo.
"""

from __future__ import annotations

import os
import shutil
import string
import subprocess
import webbrowser


APPS = {
    "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vs code": r"C:\\Users\\ASUS\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "vscode": r"C:\\Users\\ASUS\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
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

    # Websites
    "youtube": "https://www.youtube.com",
    "youtube music": "https://music.youtube.com",
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
    "docs": "https://docs.google.com/document/",
    "sheets": "https://docs.google.com/spreadsheets/",
    "slides": "https://docs.google.com/presentation/",
    "translate": "https://translate.google.com",
    "photos": "https://photos.google.com",
}


def open_app(app_name: str) -> str:
    """
    Open a desktop app or website based on a simple name.
    Handles:
    - Executables / full paths (VS Code, Chrome, etc.)
    - Commands in PATH
    - URLs in default browser
    - Windows URI schemes like ms-settings:
    """
    # normalize
    app_name = app_name.lower().strip()
    # strip trailing punctuation like "." from STT
    app_name = app_name.strip(string.punctuation)

    for key, target in APPS.items():
        # loose match: "open github.", "open my github", etc.
        if key == app_name or key in app_name:
            # URL → open via browser
            if target.startswith("http://") or target.startswith("https://"):
                webbrowser.open(target)
                return f"Opening {key} in browser."

            # Windows URI schemes (settings:, camera:, etc.)
            if target.endswith(":") and ":\\" not in target:
                # use start so Windows handles the URI
                subprocess.Popen(["start", "", target], shell=True)
                return f"Opening {key}"

            # If it's a full file path and exists
            if os.path.isabs(target) and os.path.exists(target):
                subprocess.Popen([target])
                return f"Opening {key}"

            # If it's just a command name and is in PATH
            if shutil.which(target):
                subprocess.Popen([target])
                return f"Opening {key}"

            return f"Couldn't open {key}. File or command not found."

    return f"I don't know how to open {app_name} yet."
