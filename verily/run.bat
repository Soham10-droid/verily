@echo off
REM Double-click this file to install everything and start the app (Windows).
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)
echo Installing the tools this project needs (only slow the first time)...
%PY% -m pip install -r requirements.txt
echo.
echo Starting Verily. Your browser will open in a few seconds.
echo To stop it, close this window.
%PY% -m streamlit run app.py
pause
