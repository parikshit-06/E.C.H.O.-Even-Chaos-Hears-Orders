@echo off
REM Register E.C.H.O. Assistant to run at user logon via Task Scheduler
REM Requires an existing Python installation in PATH.

set SCRIPT_DIR=%~dp0
set RUN_SCRIPT="%SCRIPT_DIR%run_background.py"

REM Allow override of pythonw path via env
if not "%ECHO_PYTHONW%"=="" (
    set PYTHON_EXE=%ECHO_PYTHONW%
) else (
    for /f "tokens=*" %%p in ('where pythonw 2^>nul') do (
        if not defined PYTHON_EXE set PYTHON_EXE="%%p"
    )
)

if "%PYTHON_EXE%"=="" (
    echo Could not find pythonw. Set ECHO_PYTHONW to full path, e.g. C:\Python311\pythonw.exe
    pause
    exit /b 1
)

echo Using pythonw: %PYTHON_EXE%
echo Script: %RUN_SCRIPT%

REM Create a scheduled task that runs on logon
REM Note: /RL lowest is not accepted on all systems; omit /RL for compatibility
schtasks /create /f /tn "ECHO_Assistant" /sc onlogon /tr "%PYTHON_EXE% %RUN_SCRIPT%" /delay 0000:10

if %errorlevel%==0 (
    echo Task 'ECHO_Assistant' created. It will start at next logon.
) else (
    echo Failed to create task. Try running this as Administrator.
)

pause
