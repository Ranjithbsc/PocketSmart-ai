@echo off
setlocal
cd /d "%~dp0"

echo [1/4] Creating virtual environment...
py -3 -m venv .venv
if errorlevel 1 goto :error

echo [2/4] Installing dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo [3/4] Creating .env...
if not exist .env copy .env.example .env >nul

echo [4/4] Setup complete.
echo.
echo Next: edit .env and add your NEW GEMINI_API_KEY, then run run_windows.bat
pause
exit /b 0

:error
echo.
echo Setup failed. Check that Python 3.11+ is installed and available as 'py'.
pause
exit /b 1
