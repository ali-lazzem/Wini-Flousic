@echo off
title Wini Flousic Launcher

echo ========================================
echo   Starting Wini Flousic...
echo ========================================

:: Backend
echo [1/3] Starting Django backend...

start "Wini Flousic Backend" cmd /k "call backend-env\Scripts\activate && python manage.py runserver"

:: Wait for backend to initialize
timeout /t 5 /nobreak > nul

:: Frontend

start "Wini Flousic Frontend" cmd /k "cd frontend && npm run dev"

:: Wait for Vite to compile
timeout /t 7 /nobreak > nul

:: Open browser
echo [3/3] Opening browser...
start http://localhost:5173

echo Done.
echo If you still see ECONNREFUSED errors, make sure the backend is running on port 8000.
pause