#!/bin/bash

# KILIMO GURU Deployment Script
# Usage: ./deploy.sh [environment]
# Environment: development (default) | production

set -e

ENVIRONMENT=${1:-development}
echo "Deploying KILIMO GURU in $ENVIRONMENT mode..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root for production
if [ "$ENVIRONMENT" = "production" ] && [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root for production deployment"
    exit 1
fi

# Update system packages
print_status "Updating system packages..."
if [ "$ENVIRONMENT" = "production" ]; then
    apt-get update && apt-get upgrade -y
fi

# Install dependencies
print_status "Installing dependencies..."
if [ "$ENVIRONMENT" = "production" ]; then
    apt-get install -y python3-pip python3-venv python3-dev nginx redis-server postgresql postgresql-contrib libpq-dev
fi

# Create virtual environment
print_status "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install Python packages
print_status "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
print_status "Setting up environment variables..."
if [ ! -f ".env" ]; then
    if [ "$ENVIRONMENT" = "production" ]; then
        print_warning "Please create .env file with production settings"
        cp .env.example .env
        nano .env
    else
        cp .env.example .env
        print_status "Created .env file from template"
    fi
fi

# Database setup
print_status "Setting up database..."
if [ "$ENVIRONMENT" = "production" ]; then
    # PostgreSQL setup
    sudo -u postgres psql -c "CREATE DATABASE kilimo_guru;" 2>/dev/null || print_warning "Database already exists"
    sudo -u postgres psql -c "CREATE USER kilimo_guru WITH PASSWORD 'kilimo_guru_password';" 2>/dev/null || print_warning "User already exists"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE kilimo_guru TO kilimo_guru;" 2>/dev/null || true
fi

# Run migrations
print_status "Running database migrations..."
python manage.py migrate

# Create superuser
print_status "Creating superuser..."
python manage.py createsuperuser --noinput 2>/dev/null || print_warning "Superuser may already exist"

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p media
mkdir -p staticfiles

# Set permissions
if [ "$ENVIRONMENT" = "production" ]; then
    print_status "Setting file permissions..."
    chown -R www-data:www-data .
    chmod -R 755 .
    chmod -R 777 media logs
fi

# Setup systemd services for production
if [ "$ENVIRONMENT" = "production" ]; then
    print_status "Setting up systemd services..."
    
    # Gunicorn service
    cat > /etc/systemd/system/kilimo-guru.service <<EOF
[Unit]
Description=KILIMO GURU Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn --access-logfile - --workers 4 --bind unix:$(pwd)/kilimo-guru.sock kilimo_guru.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

    # Celery worker service
    cat > /etc/systemd/system/kilimo-guru-celery.service <<EOF
[Unit]
Description=KILIMO GURU Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/celery -A kilimo_guru worker --loglevel=info --detach
ExecStop=$(pwd)/venv/bin/celery -A kilimo_guru control shutdown
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    # Celery beat service
    cat > /etc/systemd/system/kilimo-guru-celery-beat.service <<EOF
[Unit]
Description=KILIMO GURU Celery Beat
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/celery -A kilimo_guru beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and start services
    systemctl daemon-reload
    systemctl enable kilimo-guru
    systemctl enable kilimo-guru-celery
    systemctl enable kilimo-guru-celery-beat
    
    # Nginx configuration
    print_status "Configuring Nginx..."
    cat > /etc/nginx/sites-available/kilimo-guru <<EOF
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias $(pwd)/staticfiles/;
    }
    
    location /media/ {
        alias $(pwd)/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$(pwd)/kilimo-guru.sock;
    }
}
EOF

    # Enable nginx config
    ln -sf /etc/nginx/sites-available/kilimo-guru /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    nginx -t
    
    # Start services
    print_status "Starting services..."
    systemctl start kilimo-guru
    systemctl start kilimo-guru-celery
    systemctl start kilimo-guru-celery-beat
    systemctl restart nginx
    systemctl restart redis
    
    # Firewall configuration
    print_status "Configuring firewall..."
    ufw allow 'Nginx Full'
    ufw allow OpenSSH
    ufw --force enable
fi

# Development setup
if [ "$ENVIRONMENT" = "development" ]; then
    print_status "Development environment ready!"
    print_status "Run 'python manage.py runserver' to start the development server"
fi

print_status "Deployment complete!"
print_status "Visit: http://localhost:8000 (development) or your server IP (production)"
print_status "Admin panel: http://localhost:8000/admin/"

# Health check
print_status "Running health check..."
if [ "$ENVIRONMENT" = "production" ]; then
    sleep 2
    if systemctl is-active --quiet kilimo-guru; then
        print_status "KILIMO GURU is running successfully!"
    else
        print_error "KILIMO GURU service failed to start. Check logs with: journalctl -u kilimo-guru"
        exit 1
    fi
fi
