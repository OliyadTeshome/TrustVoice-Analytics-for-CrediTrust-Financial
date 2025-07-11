# 🏦 TrustVoice Analytics for CrediTrust Financial

A comprehensive RAG-powered financial complaints analysis platform that provides insights into consumer financial complaints using advanced natural language processing and machine learning techniques.

## 🌟 Features

### 📊 **Analytics Dashboard**
- **Real-time Metrics**: Total complaints, unique companies, product categories, and geographic coverage
- **Interactive Visualizations**: Dynamic charts and graphs using Plotly
- **Trend Analysis**: Time-series analysis of complaint patterns
- **Geographic Insights**: State-wise complaint distribution

### 🔍 **RAG-Powered Search**
- **Semantic Search**: Find similar complaints using advanced embeddings
- **Context-Aware Results**: Intelligent ranking based on complaint similarity
- **Real-time Processing**: Instant search results with detailed complaint information
- **Customizable Results**: Adjustable number of search results

### 📈 **Advanced Analytics**
- **Company Analysis**: Top companies by complaint volume
- **Product Analysis**: Complaint patterns by financial products
- **Geographic Analysis**: Regional complaint trends
- **Data Explorer**: Interactive data exploration and filtering

### 🛡️ **Data Security & Quality**
- **Data Preprocessing**: Automated cleaning and normalization
- **Duplicate Detection**: Intelligent duplicate removal
- **Missing Value Handling**: Robust data quality management
- **Privacy Protection**: Secure handling of sensitive financial data

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/OliyadTeshome/TrustVoice-Analytics-for-CrediTrust-Financial.git
   cd TrustVoice-Analytics-for-CrediTrust-Financial
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run src/app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
TrustVoice-Analytics-for-CrediTrust-Financial/
├── src/                          # Application source code
│   ├── app.py                    # Streamlit web application
│   └── rag_pipeline.py          # RAG pipeline implementation
├── data/                         # Data files
│   ├── raw/                      # Raw complaint data
│   └── filtered/                 # Processed data
├── tests/                        # Unit tests
│   ├── test_rag_pipeline.py     # RAG pipeline tests
│   └── test_streamlit_app.py    # Streamlit app tests
├── deploy/                       # Deployment scripts
│   ├── deploy.sh                 # Linux deployment
│   └── deploy.bat               # Windows deployment
├── .github/workflows/            # CI/CD pipeline
│   └── ci-cd.yml               # GitHub Actions workflow
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## 🔧 Technology Stack

### **Core Technologies**
- **Python 3.11** - Primary programming language
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Plotly** - Interactive visualizations

### **RAG Pipeline**
- **Sentence Transformers** - Text embeddings
- **Transformers** - Hugging Face models
- **PyTorch** - Deep learning framework
- **FAISS** - Vector similarity search
- **ChromaDB** - Vector database

### **Development & Testing**
- **pytest** - Testing framework
- **flake8** - Code linting
- **black** - Code formatting
- **safety** - Security scanning
- **bandit** - Security linting

## 📊 Data Sources

The application uses Consumer Financial Protection Bureau (CFPB) complaint data, including:
- **Company Information**: Financial institutions and their details
- **Product Categories**: Credit cards, mortgages, student loans, etc.
- **Complaint Narratives**: Detailed consumer complaint descriptions
- **Geographic Data**: State and regional information
- **Temporal Data**: Complaint submission dates and trends

## 🎯 Use Cases

### **For Financial Institutions**
- **Risk Assessment**: Identify potential compliance issues
- **Customer Service**: Understand common complaint patterns
- **Product Development**: Improve products based on feedback
- **Regulatory Compliance**: Monitor complaint trends

### **For Regulators**
- **Market Monitoring**: Track industry-wide trends
- **Enforcement**: Identify problematic practices
- **Policy Development**: Data-driven policy recommendations
- **Public Reporting**: Transparent complaint analysis

### **For Consumers**
- **Market Research**: Compare financial institutions
- **Complaint Resolution**: Find similar cases and outcomes
- **Financial Education**: Understand common issues
- **Advocacy**: Support consumer protection efforts

## 🚀 Deployment

### **Local Development**
```bash
# Activate environment
venv\Scripts\activate

# Run application
streamlit run src/app.py
```

### **Server Deployment**

#### **Linux (systemd)**
```bash
# Run deployment script
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

#### **Windows (NSSM)**
```cmd
# Run deployment script
deploy\deploy.bat
```

### **Cloud Deployment**

#### **Heroku**
```bash
# Create Procfile
echo "web: streamlit run src/app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create trustvoice-analytics
git push heroku main
```

#### **AWS/GCP/Azure**
- Deploy to cloud compute instances
- Use managed Python environments
- Set up load balancers and auto-scaling

## 🧪 Testing

### **Run All Tests**
```bash
pytest tests/ -v
```

### **Run with Coverage**
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### **Code Quality Checks**
```bash
# Linting
flake8 src/

# Formatting
black src/

# Security checks
safety check
bandit -r src/
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline with:

- **Automated Testing**: Multi-Python version testing
- **Code Quality**: Linting and formatting checks
- **Security Scanning**: Vulnerability and security analysis
- **Coverage Reporting**: Code coverage metrics
- **Build Automation**: Application packaging
- **Deployment**: Staging and production deployments

### **Pipeline Stages**
1. **Test Stage** - Multi-Python testing, linting, coverage
2. **Security Stage** - Vulnerability and security scanning
3. **Build Stage** - Application building and packaging
4. **Deploy Stage** - Staging and production deployments

## 📈 Performance Features

### **Optimization**
- **Vector Caching**: Efficient similarity search
- **Data Preprocessing**: Optimized data loading
- **Memory Management**: Efficient memory usage
- **Response Time**: Fast search and analysis

### **Scalability**
- **Modular Architecture**: Easy to extend and maintain
- **Component Separation**: Independent RAG pipeline
- **Configurable Parameters**: Adjustable search and analysis settings
- **Batch Processing**: Efficient handling of large datasets

## 🔒 Security & Privacy

### **Data Protection**
- **Secure Processing**: No sensitive data storage
- **Access Control**: Proper file permissions
- **Audit Logging**: Comprehensive activity tracking
- **Privacy Compliance**: GDPR and regulatory compliance

### **Application Security**
- **Input Validation**: Robust data validation
- **Error Handling**: Secure error management
- **Dependency Scanning**: Regular security updates
- **Code Security**: Security-focused development practices

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests for new functionality**
5. **Ensure all tests pass**
6. **Submit a pull request**

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 safety bandit

# Run development checks
setup-ci-cd.bat
```

## 📚 Documentation

- **[CI/CD Setup Guide](CI_CD_SETUP.md)** - Comprehensive deployment and CI/CD documentation
- **[API Documentation](docs/api.md)** - API reference and usage examples
- **[User Guide](docs/user-guide.md)** - Application usage instructions
- **[Developer Guide](docs/developer-guide.md)** - Development and contribution guidelines

## 🏆 Features in Detail

### **Dashboard Analytics**
- **Real-time Metrics**: Live updates of complaint statistics
- **Interactive Charts**: Zoom, pan, and filter capabilities
- **Export Functionality**: Download charts and data
- **Customizable Views**: User-defined dashboard layouts

### **RAG Search Engine**
- **Semantic Understanding**: Context-aware search results
- **Similarity Scoring**: Intelligent result ranking
- **Filter Options**: Company, product, date range filters
- **Export Results**: Download search results as CSV

### **Data Explorer**
- **Interactive Tables**: Sortable and filterable data views
- **Column Analysis**: Statistical summaries for each field
- **Data Profiling**: Automatic data quality assessment
- **Visualization Tools**: Built-in chart creation

## 🎯 Roadmap

### **Phase 1 (Current)**
- ✅ Basic RAG pipeline implementation
- ✅ Streamlit web application
- ✅ CI/CD pipeline setup
- ✅ Unit testing framework

### **Phase 2 (Planned)**
- 🔄 Advanced analytics dashboard
- 🔄 Real-time data processing
- 🔄 Machine learning models
- 🔄 API endpoints

### **Phase 3 (Future)**
- 📋 Multi-language support
- 📋 Mobile application
- 📋 Advanced visualization
- 📋 Predictive analytics

## 📞 Support

### **Getting Help**
- **Issues**: [GitHub Issues](https://github.com/OliyadTeshome/TrustVoice-Analytics-for-CrediTrust-Financial/issues)
- **Documentation**: [Project Wiki](https://github.com/OliyadTeshome/TrustVoice-Analytics-for-CrediTrust-Financial/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/OliyadTeshome/TrustVoice-Analytics-for-CrediTrust-Financial/discussions)

### **Contact**
- **Email**: team@trustvoice.com
- **Website**: [TrustVoice Analytics](https://trustvoice.com)
- **LinkedIn**: [TrustVoice Analytics](https://linkedin.com/company/trustvoice-analytics)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CFPB** - For providing the complaint data
- **Streamlit** - For the excellent web framework
- **Hugging Face** - For the transformer models
- **Open Source Community** - For the amazing tools and libraries

---

**Built with ❤️ by the TrustVoice Analytics Team**

*Empowering financial transparency through data-driven insights* 