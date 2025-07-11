@echo off
echo ========================================
echo TrustVoice Analytics Deployment (Windows)
echo ========================================
echo.

set APP_NAME=trustvoice-analytics
set APP_DIR=C:\opt\%APP_NAME%

echo 🚀 Starting TrustVoice Analytics deployment...
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ❌ This script should not be run as administrator
    pause
    exit /b 1
)

REM Create application directory
echo 📁 Creating application directory...
if not exist "%APP_DIR%" mkdir "%APP_DIR%"

REM Copy application files
echo 📦 Copying application files...
xcopy /E /I /Y src "%APP_DIR%\src"
copy requirements.txt "%APP_DIR%\"
copy README.md "%APP_DIR%\"
if exist data xcopy /E /I /Y data "%APP_DIR%\data"

REM Create Python virtual environment
echo 🐍 Setting up Python environment...
cd /d "%APP_DIR%"
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create Windows service (using NSSM)
echo ⚙️  Setting up Windows service...
where nssm >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  NSSM not found. Installing NSSM...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'}"
    powershell -Command "& {Expand-Archive -Path 'nssm.zip' -DestinationPath 'C:\nssm' -Force}"
    set PATH=%PATH%;C:\nssm\nssm-2.24\win64
)

REM Create service
nssm install %APP_NAME% "%APP_DIR%\venv\Scripts\python.exe" "%APP_DIR%\venv\Scripts\streamlit.exe run src/app.py --server.port=8501 --server.address=0.0.0.0"
nssm set %APP_NAME% AppDirectory "%APP_DIR%"
nssm set %APP_NAME% AppStdout "%APP_DIR%\app.log"
nssm set %APP_NAME% AppStderr "%APP_DIR%\app.log"
nssm set %APP_NAME% Start SERVICE_AUTO_START

REM Start service
echo 🔄 Starting service...
nssm start %APP_NAME%

REM Check service status
echo 📊 Checking service status...
timeout /t 3 /nobreak >nul
nssm status %APP_NAME%

echo.
echo ✅ Deployment completed successfully!
echo 🌐 Application should be available at: http://localhost:8501
echo 📋 Useful commands:
echo    nssm status %APP_NAME%
echo    nssm restart %APP_NAME%
echo    nssm stop %APP_NAME%
echo.
pause 