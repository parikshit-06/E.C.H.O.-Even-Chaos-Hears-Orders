# E.C.H.O. Background Service Setup

This guide explains how to run E.C.H.O. Assistant as a background service.

## Quick Start

### Windows
1. **Double-click** `start_background.bat`
2. The assistant will start in the background
3. Look for the **green circle with "E"** in your system tray
4. Right-click the tray icon to pause/resume or exit

### Linux/Mac
1. Make the script executable:
   ```bash
   chmod +x start_background.sh
   ```
2. Run the script:
   ```bash
   ./start_background.sh
   ```
3. Look for the tray icon in your system tray

### Python Direct
```bash
python run_background.py
```

### Custom Tray Icon (Optional)
Use your own image for the tray icon (PNG/JPG recommended 64x64):
```bash
# Windows (PowerShell) - single icon for both states
$env:ECHO_TRAY_ICON="C:\\path\\to\\icon.png"
python run_background.py

# Windows (PowerShell) - separate icons
$env:ECHO_TRAY_ICON_ON="C:\\path\\to\\listening.png"
$env:ECHO_TRAY_ICON_OFF="C:\\path\\to\\paused.png"
python run_background.py

# Linux/Mac (bash) - single icon
ECHO_TRAY_ICON="/path/to/icon.png" python run_background.py

# Linux/Mac (bash) - separate icons
ECHO_TRAY_ICON_ON="/path/to/listening.png" \
ECHO_TRAY_ICON_OFF="/path/to/paused.png" \
python run_background.py
```
If the path is invalid, the default icon is used.

#### Built-in defaults
If you place `images/ON.jpg` and `images/OFF.jpg` in the project root, they will be used automatically when no env vars are set.

## System Tray Features

The tray icon shows the current status:
- 🟢 **Green Circle** = Listening for "hey Jarvis"
- 🔴 **Red Circle** = Paused

**Right-click menu:**
- **🟢 Listening / 🔴 Paused** - Toggle listening state
- **Exit E.C.H.O.** - Stop the assistant

## Requirements

Install the required packages:
```bash
pip install pystray pillow
```

These are needed for the system tray icon functionality.

## Auto-Start on Boot

### Windows (Task Scheduler)
**Quick method (script):** Double-click `register_autostart.bat` (runs `schtasks` to register at logon).

**Manual method:**
1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click "Create Basic Task"
3. Name: "E.C.H.O. Assistant"
4. Trigger: "When I log on"
5. Action: "Start a program"
6. Program: `pythonw`
7. Arguments: `C:\Path\To\E.C.H.O\run_background.py`
8. Start in: `C:\Path\To\E.C.H.O\`
9. Finish, then right-click task → Properties → General → check "Run whether user is logged on or not"

### Linux (systemd)
Create `~/.config/systemd/user/echo-assistant.service`:
```ini
[Unit]
Description=E.C.H.O. Voice Assistant
After=sound.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/E.C.H.O/run_background.py
Restart=on-failure

[Install]
WantedBy=default.target
```

Enable and start:
```bash
systemctl --user enable echo-assistant.service
systemctl --user start echo-assistant.service
```

### Mac (launchd)
Create `~/Library/LaunchAgents/com.echo.assistant.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.echo.assistant</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/E.C.H.O/run_background.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.echo.assistant.plist
```

## Troubleshooting

### No tray icon appears
- Install dependencies: `pip install pystray pillow`
- Check that your desktop environment supports system tray icons
- Try running `python run_background.py` to see error messages

### Wake-word not working
- Check microphone permissions
- Ensure `.env` file is configured correctly
- Test with: `cd src && python -m echo_assistant.main wake`

### High CPU usage
- Consider using a smaller Whisper model in `config.py`:
  ```python
  stt_model_name: str = "tiny"  # or "base"
  ```

## Logs

View logs by checking the terminal output when running `python run_background.py` directly.

For persistent logging, modify `run_background.py`:
```python
logging.basicConfig(
    level=logging.INFO,
    filename='echo_assistant.log',
    format='%(asctime)s [%(levelname)s] %(message)s'
)
```
