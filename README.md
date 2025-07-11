# TrustVoice Analytics

**AI-powered complaint analysis and response system for CrediTrust Financial.**

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Setup & Usage](#setup--usage)
5. [Methodology](#methodology)
6. [Performance Metrics](#performance-metrics)
7. [Architecture](#architecture)
8. [Future Enhancements](#future-enhancements)
9. [Contributing](#contributing)
10. [License](#license)
11. [Contact](#contact)

---

## Overview

TrustVoice Analytics leverages Retrieval-Augmented Generation (RAG) to analyze and respond to consumer complaints from the CFPB Consumer Complaint Database. It provides actionable insights for customer service and risk management through a scalable, enterprise-ready architecture.

---

## Features

- **Complaint Analysis:** Processes and analyzes complaints across 21 product categories, focusing on credit cards, personal loans, savings accounts, and money transfers.
- **Semantic Search:** Retrieves relevant complaint data using a vector store with semantic search.
- **Real-time Responses:** Delivers high-quality responses in under 2 seconds via a Streamlit chat interface.
- **Scalable Architecture:** Optimized for CPU performance and robust deployment.

---

## Installation

### Prerequisites

- Python 3.10+
- 16GB RAM (recommended)
- 50GB+ storage for vector store
- 8+ CPU cores for optimal performance

### Dependencies

Install required packages:
```bash
pip install pandas numpy matplotlib seaborn langchain sentence-transformers transformers chromadb faiss-cpu streamlit gradio pytest flake8 black
```

---

## Setup & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/OliyadTeshome/TrustVoice-Analytics-for-CrediTrust-Financial.git
cd trustvoice-analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Data Processing

- Download the CFPB Consumer Complaint Database (9.6M+ records).
- Run the preprocessing script:
  ```bash
  python scripts/preprocess_data.py
  ```

### 4. Vector Store Setup

- Initialize the ChromaDB vector store:
  ```bash
  python scripts/setup_vector_store.py
  ```

### 5. Run the Application

- Start the Streamlit web interface:
  ```bash
  streamlit run app.py
  ```
- Access via [http://localhost:8501](http://localhost:8501)

---

## Methodology

- **Dataset:** CFPB Consumer Complaint Database (9.6M+ records)
- **Preprocessing:** Text cleaning, product filtering (4 categories), sampling (40,000 complaints)
- **Text Chunking:** Recursive/CharacterTextSplitter with 50-character overlap (163,123 chunks)
- **Embedding Model:** all-MiniLM-L6-v2 (384 dimensions)
- **Vector Store:** ChromaDB with FAISS-CPU
- **Retrieval:** Top-5 document retrieval using L2 distance
- **RAG Pipeline:** Combines semantic search, template-based response generation, and quality scoring

---

## Performance Metrics

- **Retrieval Accuracy:** 100% (test queries)
- **Response Quality:** All responses scored as high-quality (1-5 scale)
- **Response Time:** < 2 seconds per query
- **Average Context Length:** 1,500 characters

---

## Architecture

- **Data Layer:** Processes and filters CFPB dataset
- **Embedding Layer:** Generates text chunks and vectors
- **Storage Layer:** Stores vectors in ChromaDB
- **Retrieval Layer:** Semantic search and ranking
- **Generation Layer:** Formatted response creation
- **Interface Layer:** Streamlit web application

---

## Future Enhancements

### Immediate (0-3 months)
- Cloud deployment (AWS/Azure)
- Monitoring, alerting, and automated backups
- User documentation and training

### Medium-term (3-6 months)
- Advanced analytics (trend analysis, predictive modeling)
- CRM and regulatory tool integration
- Enhanced security (role-based access, encryption)

### Long-term (6-12 months)
- Fine-tuned language models for domain data
- Multi-language support and sentiment analysis
- Executive dashboards and predictive analytics

---

## Contributing

Contributions are welcome!  
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add feature"`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For inquiries, contact the project maintainers at [oliyadteshomedida@gmail.com](mailto:oliyadteshomedida@gmail.com).
