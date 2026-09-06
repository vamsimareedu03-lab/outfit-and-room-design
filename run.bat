@echo off
cd /d "%~dp0"
if not exist venv\Scripts\python.exe (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo Installing required packages...
pip install -r backend\requirements.txt
start "StyleAI" http://127.0.0.1:5000
python backend\app.py
pause
