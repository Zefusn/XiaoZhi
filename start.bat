@echo off
echo ===================================
echo Xiaozhi Label Data Web Application Startup Script
echo ===================================
echo.

echo [1/3] Checking backend dependencies...
cd backend
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing backend dependencies...
    echo Tip: If installation fails, please run install_windows_with_magic.bat script
    echo Or use precompiled wheel files for installation
    call install_windows_with_magic.bat
) else (
    echo Backend dependencies installed
)

echo.
echo [2/3] Starting backend service...
start cmd /k "cd /d %cd% && echo Starting Flask backend service... && python app.py"

echo.
echo [3/3] Waiting for backend to start (5 seconds)...
timeout /t 5 /nobreak >nul

cd ..
echo.
echo Checking frontend dependencies...
if not exist "node_modules" (
    echo Installing frontend dependencies, please wait...
    call npm install
) else (
    echo Frontend dependencies installed
)

echo.
echo Starting frontend development server...
start cmd /k "cd /d %cd% && echo Starting Vue frontend service... && npm run dev"

echo.
echo ===================================
echo Startup completed!
echo Backend address: http://localhost:5000
echo Frontend address: http://localhost:5173
echo ===================================
echo.
echo Press any key to exit...
pause >nul
