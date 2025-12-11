#!/bin/bash
# Start E.C.H.O. Assistant in background mode (Linux/Mac)
# Run this script to start E.C.H.O. silently in the background

cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Start in background
nohup python3 run_background.py > /dev/null 2>&1 &

echo "🎤 E.C.H.O. Assistant started in background!"
echo "📍 Check your system tray for the icon"
echo "💡 PID: $!"
