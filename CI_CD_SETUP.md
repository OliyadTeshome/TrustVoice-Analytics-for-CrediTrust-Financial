# CI/CD Setup for TrustVoice Analytics

This document describes the complete CI/CD pipeline setup for the TrustVoice Analytics project.

## 🚀 Overview

The CI/CD pipeline is built using GitHub Actions and includes:

- **Testing**: Multi-Python version testing with pytest
- **Code Quality**: Linting with flake8 and formatting with black
- **Security**: Security scanning with safety and bandit
- **Coverage**: Code coverage reporting with Codecov
- **Build**: Application building and packaging
- **Deployment**: Staging and production deployments
- **Direct Deployment**: Server deployment scripts for Linux and Windows

## 📁 Pipeline Structure

```
.github/workflows/
├── ci-cd.yml              # Main CI/CD workflow
├── deploy-staging.yml     # Staging deployment (optional)
└── deploy-production.yml  # Production deployment (optional)

deploy/
├── deploy.sh              # Linux deployment script
└── deploy.bat             # Windows deployment script

tests/
├── __init__.py
├── test_rag_pipeline.py   # RAG pipeline tests
└── test_streamlit_app.py  # Streamlit app tests

Configuration Files:
├── .flake8               # Linting configuration
├── pytest.ini           # Test configuration
├── pyproject.toml       # Modern Python configuration
└── requirements.txt     # Dependencies
```

## 🔧 Pipeline Stages

### 1. Test Stage
- **Trigger**: Push to main/develop or pull requests
- **Python Versions**: 3.9, 3.10, 3.11
- **Actions**:
  - Install dependencies
  - Run linting (flake8)
  - Run tests (pytest)
  - Generate coverage reports
  - Upload to Codecov

### 2. Security Stage
- **Dependencies**: test stage
- **Actions**:
  - Run safety checks (vulnerability scanning)
  - Run bandit (security linting)
  - Generate security reports

### 3. Build Stage
- **Trigger**: Only on main branch
- **Dependencies**: test + security stages
- **Actions**:
  - Build application
  - Create deployment package
  - Upload artifacts

### 4. Deploy Stages
- **Staging**: Deploy to staging environment (develop branch)
- **Production**: Deploy to production environment (main branch)

## 🛠️ Local Development

### Running Tests Locally

```bash
# Activate virtual environment
venv\Scripts\activate

# Run all tests
pytest

# Run specific test file
pytest tests/test_rag_pipeline.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run linting
flake8 src/

# Format code
black src/
```

### Running Security Checks

```bash
# Install security tools
pip install safety bandit

# Run safety check
safety check

# Run bandit
bandit -r src/
```

## 🚀 Direct Deployment

### Local Development

```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/app.py
```

### Server Deployment

```bash
# On your server, create a Python environment
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Run as a service (Linux example)
sudo systemctl enable trustvoice-analytics
sudo systemctl start trustvoice-analytics
```

## 🔐 Environment Configuration

### GitHub Secrets Required

For full CI/CD functionality, set these secrets in your GitHub repository:

```bash
# For Codecov integration
CODECOV_TOKEN=your_codecov_token

# For deployment (if using cloud platforms)
DEPLOY_KEY=your_deployment_key
STAGING_HOST=your_staging_host
PRODUCTION_HOST=your_production_host
```

### Environment Variables

```bash
# Application configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Database (if using)
POSTGRES_PASSWORD=your_db_password
DATABASE_URL=postgresql://user:pass@host:port/db
```

## 📊 Monitoring and Reporting

### Code Coverage

The pipeline generates coverage reports in multiple formats:
- **Terminal**: Coverage summary in CI logs
- **HTML**: Detailed coverage report (uploaded as artifact)
- **XML**: Codecov-compatible format

### Security Reports

- **Safety**: Vulnerability scanning report
- **Bandit**: Security linting report (JSON format)

### Build Artifacts

- **Application Package**: `trustvoice-analytics.tar.gz`
- **Coverage Reports**: HTML and XML formats
- **Security Reports**: JSON format

## 🚀 Deployment Options

### 1. Direct Server Deployment (Recommended)

```bash
# On your server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0
```

### 2. Cloud Platform Deployment

#### Heroku
```bash
# Create Procfile
echo "web: streamlit run src/app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create trustvoice-analytics
git push heroku main
```

#### AWS/GCP/Azure
- Deploy directly to cloud compute instances
- Use managed Python environments
- Set up load balancers and auto-scaling

### 3. Systemd Service (Linux)

```bash
# Create service file
sudo nano /etc/systemd/system/trustvoice-analytics.service

# Service content:
[Unit]
Description=TrustVoice Analytics
After=network.target

[Service]
Type=simple
User=trustvoice
WorkingDirectory=/opt/trustvoice-analytics
Environment=PATH=/opt/trustvoice-analytics/venv/bin
ExecStart=/opt/trustvoice-analytics/venv/bin/streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable trustvoice-analytics
sudo systemctl start trustvoice-analytics
```

## 🔄 Pipeline Customization

### Adding New Tests

1. Create test file in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Use pytest markers for categorization
4. Add to CI workflow if needed

### Adding New Dependencies

1. Update `requirements.txt`
2. Update `pyproject.toml` dependencies
3. Test locally with `pip install -r requirements.txt`
4. Commit and push to trigger CI

### Modifying Deployment

1. Update requirements.txt for new dependencies
2. Modify deployment scripts for new services
3. Update CI/CD workflow for new deployment steps
4. Test deployment locally first

## 🐛 Troubleshooting

### Common Issues

1. **Test Failures**
   ```bash
   # Run tests with verbose output
   pytest -v --tb=long
   
   # Check specific test
   pytest tests/test_rag_pipeline.py::TestRAGPipeline::test_pipeline_initialization -v
   ```

2. **Linting Errors**
   ```bash
   # Check specific file
   flake8 src/rag_pipeline.py
   
   # Auto-format code
   black src/
   ```

3. **Build Issues**
   ```bash
   # Check Python environment
   python --version
   pip list
   
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

4. **Deployment Issues**
   ```bash
   # Check application logs
   tail -f /var/log/trustvoice-analytics.log
   
   # Check service status
   sudo systemctl status trustvoice-analytics
   
   # Check if port is listening
   netstat -tlnp | grep 8501
   ```

### Debug Mode

Enable debug mode for local development:

```bash
# Set debug environment
export STREAMLIT_DEBUG=true

# Run with debug
streamlit run src/app.py --logger.level=debug
```

## 📈 Performance Optimization

### CI/CD Optimization

- **Caching**: Dependencies cached between runs
- **Parallel Jobs**: Tests run in parallel across Python versions
- **Conditional Jobs**: Security and build only run when needed

### Application Optimization

- **Process Management**: Systemd service for automatic restarts
- **Health Checks**: Application-level health monitoring
- **Resource Monitoring**: System-level resource monitoring

## 🔒 Security Considerations

### Code Security

- **Dependency Scanning**: Safety checks for vulnerabilities
- **Code Security**: Bandit for security linting
- **Secret Management**: GitHub secrets for sensitive data

### Runtime Security

- **Service User**: Application runs as dedicated user
- **File Permissions**: Proper file and directory permissions
- **Network Security**: Port exposure limited to necessary

## 📝 Best Practices

1. **Always test locally before pushing**
2. **Use meaningful commit messages**
3. **Review security reports regularly**
4. **Monitor application health**
5. **Keep dependencies updated**
6. **Document configuration changes**

## 🎯 Next Steps

1. **Set up GitHub secrets** for full CI/CD functionality
2. **Configure deployment environments** (staging/production)
3. **Set up monitoring** (logs, metrics, alerts)
4. **Implement database integration** if needed
5. **Add performance testing** to the pipeline
6. **Set up automated dependency updates**

---

For questions or issues with the CI/CD setup, please refer to the GitHub Actions documentation or create an issue in the repository. 