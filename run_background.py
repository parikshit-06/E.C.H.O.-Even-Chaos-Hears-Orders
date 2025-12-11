#!/usr/bin/env python
"""
run_background.py
Run E.C.H.O. Assistant as a background service with system tray.

Usage:
    python run_background.py
    
The assistant will run in the background with a system tray icon.
Right-click the tray icon to pause/resume or exit.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from echo_assistant.config import load_config
from echo_assistant.runtime.wake_listener import run_wake_listener
from echo_assistant.ui.tray import TrayIcon
import threading

# Suppress console output for cleaner background operation
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors
    format='[%(levelname)s] %(message)s'
)

def main():
    """Run E.C.H.O. in background with system tray."""
    config = load_config()
    
    print("Starting E.C.H.O. Assistant in background mode...")
    print("System tray icon will appear shortly")
    print("Right-click the tray icon to pause or exit")
    print("Say 'hey Jarvis' to activate\n")
    
    # Flag to control wake listener
    should_exit = False
    
    def exit_handler():
        nonlocal should_exit
        should_exit = True
        print("\n E.C.H.O. Assistant shutting down...")
        os._exit(0)
    
    # Optional custom tray icons via env vars
    icon_path = os.getenv("ECHO_TRAY_ICON")  # single icon for both states
    icon_path_on = os.getenv("ECHO_TRAY_ICON_ON")  # listening
    icon_path_off = os.getenv("ECHO_TRAY_ICON_OFF")  # paused

    def normalize(path: str | None) -> str | None:
        if not path:
            return None
        p = Path(path).expanduser()
        return str(p) if p.exists() else None

    icon_path = normalize(icon_path)
    icon_path_on = normalize(icon_path_on)
    icon_path_off = normalize(icon_path_off)

    # Defaults: use images/ON.jpg and images/OFF.jpg if present and no env overrides
    images_dir = Path(__file__).parent / "images"
    if not icon_path_on:
        default_on = images_dir / "ON.jpg"
        if default_on.exists():
            icon_path_on = str(default_on)
    if not icon_path_off:
        default_off = images_dir / "OFF.jpg"
        if default_off.exists():
            icon_path_off = str(default_off)

    for name, val in [("ECHO_TRAY_ICON", icon_path), ("ECHO_TRAY_ICON_ON", icon_path_on), ("ECHO_TRAY_ICON_OFF", icon_path_off)]:
        if os.getenv(name) and val is None:
            print(f"Warning: {name} file not found, falling back to default icon.")

    # Create tray icon
    tray = TrayIcon(
        on_exit=exit_handler,
        icon_path=icon_path,
        icon_path_on=icon_path_on,
        icon_path_off=icon_path_off,
    )
    
    # Run wake listener in a separate thread
    def run_listener():
        try:
            run_wake_listener(config)
        except (KeyboardInterrupt, SystemExit):
            pass
        except Exception as e:
            print(f"Error in wake listener: {e}")
            import traceback
            traceback.print_exc()
    
    listener_thread = threading.Thread(target=run_listener, daemon=True)
    listener_thread.start()
    
    # Run tray icon (blocking - keeps the app alive)
    try:
        tray.run()
    except KeyboardInterrupt:
        print("\nE.C.H.O. Assistant stopped")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
