# Deployment Guide

## 📚 Table of Contents

- [Prerequisites](#-prerequisites)
- [Local Development Setup](#-local-development-setup)
- [Production Deployment](#-production-deployment)
- [Docker Deployment](#-docker-deployment)
- [Cloud Deployment](#-cloud-deployment)
- [Monitoring and Maintenance](#-monitoring-and-maintenance)
- [Troubleshooting](#-troubleshooting)

## 🔧 Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows (with WSL)
- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB, recommended 16GB+
- **Storage**: 10GB+ free space for models and data
- **Network**: Stable internet connection for model downloads

### External Dependencies

- **Ollama**: Running locally or accessible via network
  - Required models: `nomic-embed-text`, `llama3.2:3b`
  - Installation: https://ollama.com/download

- **PDF Documents**: Dataset in `rag-dataset/` directory
  - Minimum: 1 PDF file
  - Recommended: Multiple PDFs for better results

## 🏠 Local Development Setup

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-org/rag-pdf-chatbot.git
cd rag-pdf-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .[dev]

# Setup pre-commit hooks
pre-commit install
```

### 2. Ollama Setup

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Key Configuration Options:**
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434

# Document Processing
DATASET_PATH=./rag-dataset

# Vector Store
SAVE_VECTOR_STORE=true
VECTOR_STORE_PATH=./health_supplements
```

### 4. First Run

```bash
# Build vector store and test
python -m src.main --rebuild --question "What is RAG?"
```

### 5. Development Workflow

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Lint code
ruff check src/
black src/

# Format code
black src/
isort src/
```

## 🚀 Production Deployment

### 1. Server Preparation

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install system dependencies
sudo apt install build-essential -y
```

### 2. Application Deployment

```bash
# Create application user
sudo useradd -m -s /bin/bash raguser
sudo su - raguser

# Clone repository
git clone https://github.com/your-org/rag-pdf-chatbot.git
cd rag-pdf-chatbot

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install production dependencies
pip install -e .

# Configure environment
cp .env.example .env
nano .env  # Edit for production settings
```

### 3. Data Setup

```bash
# Create data directory
mkdir -p data/rag-dataset

# Copy your PDF documents
cp /path/to/your/pdfs/* data/rag-dataset/

# Update configuration
echo "DATASET_PATH=./data/rag-dataset" >> .env
echo "VECTOR_STORE_PATH=./data/vector-store" >> .env
```

### 4. Ollama Setup (Production)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Create systemd service
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=raguser
Group=raguser
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF

# Enable and start service
sudo systemctl enable ollama
sudo systemctl start ollama

# Pull models
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

### 5. Application Service

```bash
# Create systemd service
sudo tee /etc/systemd/system/rag-chatbot.service > /dev/null <<EOF
[Unit]
Description=RAG PDF Chatbot
After=network.target ollama.service

[Service]
Type=simple
User=raguser
Group=raguser
WorkingDirectory=/home/raguser/rag-pdf-chatbot
Environment=PATH=/home/raguser/rag-pdf-chatbot/venv/bin
ExecStart=/home/raguser/rag-pdf-chatbot/venv/bin/python -m src.main --interactive
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable rag-chatbot
sudo systemctl start rag-chatbot
```

### 6. Nginx Reverse Proxy (Optional)

```bash
# Install Nginx
sudo apt install nginx -y

# Configure site
sudo tee /etc/nginx/sites-available/rag-chatbot > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/rag-chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🐳 Docker Deployment

### 1. Dockerfile

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/

# Create data directories
RUN mkdir -p data/rag-dataset data/vector-store

# Copy entrypoint script
COPY scripts/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose port (if using web interface)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "from src import RAGPDFChatbot; chatbot = RAGPDFChatbot(); chatbot.initialize(); print('OK')"

ENTRYPOINT ["docker-entrypoint.sh"]
```

### 2. Docker Compose

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

  rag-chatbot:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - DATASET_PATH=/app/data/rag-dataset
      - VECTOR_STORE_PATH=/app/data/vector-store
    restart: unless-stopped

volumes:
  ollama_data:
```

### 3. Docker Entrypoint

```bash
#!/bin/bash

# Wait for Ollama to be ready
echo "Waiting for Ollama..."
while ! curl -s http://ollama:11434/api/tags > /dev/null; do
  sleep 2
done

# Pull models
echo "Pulling models..."
ollama pull nomic-embed-text
ollama pull llama3.2:3b

# Start application
echo "Starting RAG Chatbot..."
exec python -m src.main --interactive
```

### 4. Build and Run

```bash
# Build and start
docker-compose up --build

# Or run manually
docker build -t rag-chatbot .
docker run -p 8000:8000 rag-chatbot
```

## ☁️ Cloud Deployment

### AWS EC2 Deployment

```bash
# Launch EC2 instance (t3.large or better recommended)
# Ubuntu 22.04 LTS, 16GB RAM minimum

# Security group settings:
# - SSH (22) from your IP
# - HTTP (80) and HTTPS (443) if using web interface
# - Custom TCP (11434) for Ollama if needed internally

# After SSH into instance, follow production deployment steps
```

### Google Cloud Run

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/rag-chatbot', '.']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/rag-chatbot']

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - run
      - deploy
      - rag-chatbot
      - --image=gcr.io/$PROJECT_ID/rag-chatbot
      - --platform=managed
      - --region=us-central1
      - --allow-unauthenticated
      - --memory=4Gi
      - --cpu=2
```

### Heroku Deployment

```yaml
# Procfile
web: python -m src.main --interactive

# requirements.txt (Heroku-specific)
-r requirements.txt
gunicorn==21.2.0
```

## 📊 Monitoring and Maintenance

### 1. Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/rag-chatbot.log'),
        logging.StreamHandler()
    ]
)
```

### 2. Health Checks

```bash
# Application health check
curl -f http://localhost:8000/health || exit 1

# Ollama health check
curl -f http://localhost:11434/api/tags || exit 1
```

### 3. Monitoring Commands

```bash
# Check application status
sudo systemctl status rag-chatbot

# View application logs
sudo journalctl -u rag-chatbot -f

# Check resource usage
htop
df -h
free -h

# Ollama status
ollama list
ollama ps
```

### 4. Backup Strategy

```bash
# Backup vector store and configuration
tar -czf backup-$(date +%Y%m%d).tar.gz \
    data/vector-store/ \
    .env \
    logs/

# Automated backup script
#!/bin/bash
BACKUP_DIR="/var/backups/rag-chatbot"
mkdir -p $BACKUP_DIR

tar -czf $BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).tar.gz \
    -C /home/raguser/rag-pdf-chatbot \
    data/vector-store .env logs

# Keep only last 7 backups
cd $BACKUP_DIR
ls -t backup-*.tar.gz | tail -n +8 | xargs rm -f
```

### 5. Updates

```bash
# Update application
cd /home/raguser/rag-pdf-chatbot
git pull origin main
source venv/bin/activate
pip install -e .

# Restart service
sudo systemctl restart rag-chatbot

# Update Ollama models
ollama pull nomic-embed-text:latest
ollama pull llama3.2:3b:latest
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Ollama Connection Issues

```bash
# Check if Ollama is running
ps aux | grep ollama

# Check Ollama API
curl http://localhost:11434/api/tags

# Restart Ollama
sudo systemctl restart ollama

# Check logs
sudo journalctl -u ollama -f
```

#### 2. Vector Store Issues

```bash
# Rebuild vector store
rm -rf data/vector-store/
python -m src.main --rebuild

# Check disk space
df -h
```

#### 3. Memory Issues

```bash
# Check memory usage
free -h

# Monitor process memory
ps aux --sort=-%mem | head

# Increase swap space if needed
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

#### 4. Performance Issues

```bash
# Profile application
python -m cProfile -s time -m src.main --question "test question"

# Check CPU usage
top -p $(pgrep -f "python -m src.main")

# Optimize configuration
# Reduce chunk_size, k, fetch_k for lower memory usage
```

#### 5. PDF Processing Issues

```bash
# Check PDF files
file data/rag-dataset/*.pdf

# Validate PDF content
python -c "
import fitz
doc = fitz.open('data/rag-dataset/sample.pdf')
print(f'Pages: {len(doc)}')
print(f'Text length: {len(doc[0].get_text())}')
"
```

### Debug Mode

```bash
# Run with debug logging
LOG_LEVEL=DEBUG python -m src.main --question "test"

# Check configuration
python -c "from src.config import config; print(config)"
```

### Getting Help

1. Check application logs: `tail -f logs/rag-chatbot.log`
2. Check system logs: `sudo journalctl -u rag-chatbot -f`
3. Review configuration: `cat .env`
4. Test components individually:

```bash
# Test document processing
python -c "
from src.document_processor import DocumentProcessor
processor = DocumentProcessor()
docs = processor.process_documents()
print(f'Processed {len(docs)} documents')
"

# Test vector store
python -c "
from src.vector_store import VectorStoreManager
manager = VectorStoreManager()
print('Vector store initialized successfully')
"
```

## 📞 Support

For deployment issues:
1. Check the [troubleshooting section](#-troubleshooting)
2. Review [GitHub Issues](https://github.com/your-org/rag-pdf-chatbot/issues)
3. Check application and system logs
4. Provide detailed error messages and configuration

---

**🚀 Happy Deploying!**
