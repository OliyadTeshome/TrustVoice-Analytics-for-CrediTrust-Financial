@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Running environment test...
python test_environment.py
pause 