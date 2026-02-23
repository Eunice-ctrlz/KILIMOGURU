# KILIMO GURU - Installation Guide

## System Requirements

- Python 3.9 or higher
- PostgreSQL 12+ (optional, SQLite works for development)
- Redis 6+ (optional, for caching and Celery)
- Node.js 16+ (optional, for frontend build tools)

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/kilimo-guru.git
cd kilimo-guru

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

Required environment variables:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata fixtures/initial_data.json
```

### 4. Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/

## Production Deployment

### Using Docker (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Manual Production Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

2. **Configure PostgreSQL:**
```bash
sudo -u postgres psql
CREATE DATABASE kilimo_guru;
CREATE USER kilimo_guru WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE kilimo_guru TO kilimo_guru;
\q
```

3. **Update .env:**
```
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgres://kilimo_guru:your-password@localhost:5432/kilimo_guru
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

4. **Run migrations and collect static:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

5. **Start with Gunicorn:**
```bash
gunicorn kilimo_guru.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/kilimo-guru;
    }
    location /media/ {
        root /path/to/kilimo-guru;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/kilimo-guru/kilimo-guru.sock;
    }
}
```

### SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## External Service Integration

### M-Pesa (Safaricom Daraja)

1. Register at https://developer.safaricom.co.ke/
2. Create an app
3. Get Consumer Key and Consumer Secret
4. Add to .env:
```
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your-key
MPESA_CONSUMER_SECRET=your-secret
MPESA_PASSKEY=your-passkey
MPESA_SHORTCODE=174379
MPESA_CALLBACK_URL=https://yourdomain.com/finance/mpesa/callback/
```

### Africa's Talking SMS

1. Register at https://africastalking.com/
2. Get API key
3. Add to .env:
```
AT_USERNAME=your-username
AT_API_KEY=your-api-key
AT_SENDER_ID=KILIMOGURU
```

### Weather API

1. Register at https://openweathermap.org/api
2. Get API key
3. Add to .env:
```
WEATHER_API_KEY=your-api-key
```

## Troubleshooting

### Common Issues

1. **Migration errors:**
```bash
python manage.py migrate --run-syncdb
```

2. **Static files not loading:**
```bash
python manage.py collectstatic --clear --noinput
```

3. **Permission errors:**
```bash
chmod -R 755 /path/to/kilimo-guru
chown -R www-data:www-data /path/to/kilimo-guru
```

4. **Celery not working:**
```bash
# Start Celery worker
celery -A kilimo_guru worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A kilimo_guru beat --loglevel=info
```

## Maintenance

### Backup Database

```bash
# PostgreSQL
pg_dump kilimo_guru > backup.sql

# SQLite
cp db.sqlite3 backup.sqlite3
```

### Update Application

```bash
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Monitor Logs

```bash
# Django logs
tail -f logs/kilimo_guru.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log

# Systemd logs
sudo journalctl -u gunicorn -f
```

## Support

For support, contact:
- Email: support@kilimoguru.co.ke
- Phone: +254 700 000 000
- WhatsApp: +254 700 000 000
