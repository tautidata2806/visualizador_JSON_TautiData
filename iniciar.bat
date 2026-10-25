@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m streamlit run visualizador_json_TautiData.py
) else (
  python -m streamlit run visualizador_json_TautiData.py
)
pause
