@echo off
REM Start E.C.H.O. Assistant in background mode (Windows)
REM Double-click this file to run E.C.H.O. silently in the background

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Start in background (no console window after initial launch)
start /B pythonw run_background.py

echo E.C.H.O. Assistant started in background!
echo Check your system tray for the icon.
timeout /t 3 >nul
