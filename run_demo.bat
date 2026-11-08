@echo off
title SCANNAI — Cybercrime ^& Scam Awareness Intelligence
echo ===============================================================================
echo                SCANNAI — Team ROCKERZ Demonstration Launcher
echo ===============================================================================
echo.
echo [1/3] Starting SCANNAI Backend Engine on http://127.0.0.1:8000 ...
start "SCANNAI Backend (FastAPI)" /min cmd /c "cd backend && .venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"

echo [2/3] Waiting for backend engine initialization ...
timeout /t 3 /nobreak >nul

echo [3/3] Starting SCANNAI Frontend Dashboard on http://127.0.0.1:5173 ...
start "SCANNAI Frontend (Vite)" /min cmd /c "cd frontend && npm run dev"

echo.
echo ===============================================================================
echo SCANNAI is running! Opening browser to http://127.0.0.1:5173 ...
echo ===============================================================================
echo.
start http://127.0.0.1:5173

echo Press any key to stop all SCANNAI processes and exit...
pause >nul

echo Stopping SCANNAI servers...
taskkill /FI "WINDOWTITLE eq SCANNAI Backend*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq SCANNAI Frontend*" /T /F >nul 2>&1
echo Done!
