@echo off
echo ========================================
echo TrustVoice Analytics CI/CD Setup
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing development dependencies...
pip install pytest pytest-cov black flake8 safety bandit

echo.
echo Running code formatting...
black src/ tests/

echo.
echo Running linting...
flake8 src/ tests/

echo.
echo Running security checks...
safety check
bandit -r src/ -f json -o bandit-report.json

echo.
echo Running tests with coverage...
pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

echo.
echo ========================================
echo CI/CD Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Commit and push your changes to GitHub
echo 2. Check the Actions tab in your repository
echo 3. Set up GitHub secrets if needed
echo 4. Use deployment scripts for server deployment
echo.
echo For more information, see CI_CD_SETUP.md
pause 