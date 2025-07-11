#!/bin/bash

# TrustVoice Analytics Deployment Script
# This script deploys the application to a server

set -e  # Exit on any error

# Configuration
APP_NAME="trustvoice-analytics"
APP_DIR="/opt/$APP_NAME"
SERVICE_USER="trustvoice"
SERVICE_FILE="/etc/systemd/system/$APP_NAME.service"
LOG_FILE="/var/log/$APP_NAME.log"

echo "🚀 Starting TrustVoice Analytics deployment..."

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   exit 1
fi

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
echo "📦 Copying application files..."
cp -r src/ $APP_DIR/
cp requirements.txt $APP_DIR/
cp README.md $APP_DIR/
cp -r data/ $APP_DIR/ 2>/dev/null || echo "⚠️  Data directory not found, skipping"

# Create Python virtual environment
echo "🐍 Setting up Python environment..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create service user if it doesn't exist
echo "👤 Setting up service user..."
sudo useradd -r -s /bin/false $SERVICE_USER 2>/dev/null || echo "User $SERVICE_USER already exists"

# Create systemd service file
echo "⚙️  Creating systemd service..."
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=TrustVoice Analytics
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/streamlit run src/app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=10
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE

[Install]
WantedBy=multi-user.target
EOF

# Set proper permissions
echo "🔐 Setting permissions..."
sudo chown -R $SERVICE_USER:$SERVICE_USER $APP_DIR
sudo chmod +x $APP_DIR/venv/bin/streamlit

# Create log file
sudo touch $LOG_FILE
sudo chown $SERVICE_USER:$SERVICE_USER $LOG_FILE

# Reload systemd and enable service
echo "🔄 Enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl start $APP_NAME

# Check service status
echo "📊 Checking service status..."
sleep 3
sudo systemctl status $APP_NAME --no-pager

echo "✅ Deployment completed successfully!"
echo "🌐 Application should be available at: http://localhost:8501"
echo "📋 Useful commands:"
echo "   sudo systemctl status $APP_NAME"
echo "   sudo systemctl restart $APP_NAME"
echo "   sudo journalctl -u $APP_NAME -f" 