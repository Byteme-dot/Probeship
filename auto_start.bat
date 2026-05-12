@echo off

echo ======================================
echo Starting PROBESHIP...
echo ======================================

cd /d %~dp0

REM ---------------- BACKEND ----------------

start /min cmd /c start_backend.bat

timeout /t 5 > nul

REM ---------------- FRONTEND ----------------

start /min cmd /c start_frontend.bat

timeout /t 2 > nul

echo.
echo ======================================
echo PROBESHIP is now running!
echo.
echo Frontend:
echo http://localhost:5500
echo.
echo Backend:
echo http://127.0.0.1:5000
echo ======================================
echo.

pause