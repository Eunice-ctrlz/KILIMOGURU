# KILIMO GURU - Project Structure

## Overview

KILIMO GURU is a comprehensive Django-based agricultural management system for Kenyan farmers. The project follows Django's best practices with a modular app architecture.

## Directory Structure

```
kilimo_guru/
├── kilimo_guru/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI application
│   ├── asgi.py              # ASGI application
│   └── celery.py            # Celery configuration
│
├── accounts/                 # User authentication & management
│   ├── models.py            # Custom User model, OTP, Devices
│   ├── views.py             # Registration, login, profile views
│   ├── forms.py             # Authentication forms
│   ├── urls.py              # Account URLs
│   ├── admin.py             # Admin configuration
│   └── signals.py           # User signals
│
├── farmers/                  # Farmer profile & farm management
│   ├── models.py            # FarmerProfile, FarmParcel, FarmingHistory
│   ├── views.py             # Dashboard, profile, parcel views
│   ├── forms.py             # Farmer forms
│   ├── urls.py              # Farmer URLs
│   ├── admin.py             # Admin configuration
│   └── context_processors.py # Template context processors
│
├── crops/                    # Crop & livestock management
│   ├── models.py            # Crop, FarmerCrop, PestDisease, Livestock
│   ├── views.py             # Crop management views
│   ├── forms.py             # Crop forms
│   ├── urls.py              # Crop URLs
│   └── admin.py             # Admin configuration
│
├── marketplace/              # Buy/sell platform
│   ├── models.py            # ProduceListing, MarketPrice, Transaction
│   ├── views.py             # Marketplace views
│   ├── forms.py             # Marketplace forms
│   ├── urls.py              # Marketplace URLs
│   └── admin.py             # Admin configuration
│
├── weather/                  # Weather & climate alerts
│   ├── models.py            # WeatherData, ClimateAlert
│   ├── views.py             # Weather views
│   ├── forms.py             # Weather forms
│   ├── urls.py              # Weather URLs
│   └── admin.py             # Admin configuration
│
├── finance/                  # M-Pesa, loans, insurance
│   ├── models.py            # MPesaTransaction, Loan, Insurance
│   ├── views.py             # Finance views
│   ├── forms.py             # Finance forms
│   ├── urls.py              # Finance URLs
│   └── admin.py             # Admin configuration
│
├── advisory/                 # E-learning & expert consultation
│   ├── models.py            # AdvisoryArticle, Webinar, Consultation
│   ├── views.py             # Advisory views
│   ├── forms.py             # Advisory forms
│   ├── urls.py              # Advisory URLs
│   └── admin.py             # Admin configuration
│
├── analytics/                # Data analytics & reports
│   ├── models.py            # FarmerAnalytics, MarketTrend
│   ├── views.py             # Analytics views
│   ├── urls.py              # Analytics URLs
│   └── admin.py             # Admin configuration
│
├── api/                      # REST API
│   ├── views.py             # API viewsets
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # API URLs
│   └── apps.py              # API app config
│
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── home.html            # Homepage
│   ├── accounts/            # Account templates
│   ├── farmers/             # Farmer templates
│   └── ...
│
├── static/                   # Static files
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   │   └── sw.js            # Service Worker for PWA
│   ├── images/              # Images
│   └── manifest.json        # PWA manifest
│
├── media/                    # User-uploaded files
│
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

## Apps Overview

### 1. accounts
- Custom User model with phone number authentication
- OTP verification for phone verification
- User device tracking for offline sync
- Profile management

### 2. farmers
- Farmer profile with farm details
- Farm parcel management with GPS boundaries
- Farming history for crop rotation
- Credit history for credit scoring
- KIAMIS integration support

### 3. crops
- Crop database with planting calendars
- Farmer crop tracking
- Pest and disease database
- AI-powered pest/disease detection
- Livestock management

### 4. marketplace
- Produce listings for farmers
- Livestock listings
- Market prices from major Kenyan markets
- Buyer inquiries and matching
- Transaction management

### 5. weather
- Weather data storage
- Weather forecasts
- Climate alerts (drought, flood warnings)
- User subscriptions for alerts
- Irrigation advice

### 6. finance
- M-Pesa transaction processing
- Loan products and applications
- Insurance products and policies
- Wallet management
- Credit scoring integration

### 7. advisory
- Advisory articles and content
- Webinar management
- Expert consultations
- FAQ system
- Daily farming tips
- Tele-veterinary consultations

### 8. analytics
- Farmer performance analytics
- Market trends analysis
- System metrics
- Custom reports

### 9. api
- REST API endpoints
- DRF serializers
- API authentication

## Key Features

1. **Mobile-First Design**: Responsive UI optimized for smartphones
2. **Offline Support**: PWA with service worker for offline functionality
3. **M-Pesa Integration**: Full payment processing via Safaricom API
4. **SMS Notifications**: Africa's Talking integration
5. **Weather API**: Real-time weather data
6. **KIAMIS Integration**: Government farmer registry sync
7. **Multi-language**: English, Swahili, and local languages
8. **Credit Scoring**: Data-driven credit assessment
9. **AI Features**: Pest/disease detection from photos
10. **Analytics**: Comprehensive reporting and dashboards

## Database Models

### Core Models
- **User**: Custom user with phone authentication
- **FarmerProfile**: Extended farmer information
- **FarmParcel**: Individual farm sections with GPS
- **Crop**: Crop database
- **FarmerCrop**: Farmer's planted crops
- **ProduceListing**: Marketplace listings
- **MarketPrice**: Real-time market prices
- **WeatherData**: Weather information
- **ClimateAlert**: Weather alerts
- **MPesaTransaction**: Payment records
- **LoanApplication**: Loan requests
- **InsurancePolicy**: Insurance coverage

## API Endpoints

### Authentication
- `POST /api/auth/login/`
- `POST /api/auth/logout/`

### Resources
- `GET /api/crops/`
- `GET /api/produce/`
- `GET /api/weather/`
- `GET /api/farmer/profile/`
- `GET /api/market/prices/`
- `GET /api/alerts/`

## External Integrations

1. **M-Pesa (Safaricom Daraja)**
   - STK Push payments
   - C2B transactions
   - B2C disbursements

2. **Africa's Talking**
   - SMS notifications
   - USSD support

3. **OpenWeatherMap**
   - Weather data
   - Forecasts

4. **KIAMIS**
   - Farmer registry sync
   - Subsidy tracking

## Deployment Options

1. **Docker** (Recommended)
   ```bash
   docker-compose up -d
   ```

2. **Traditional**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. **Cloud Platforms**
   - AWS Elastic Beanstalk
   - Google Cloud Run
   - Heroku
   - DigitalOcean App Platform

## Security Features

- CSRF protection
- XSS prevention
- SQL injection protection
- Secure password hashing
- OTP verification
- Rate limiting
- HTTPS enforcement

## Performance Optimizations

- Database indexing
- Query optimization
- Caching with Redis
- Static file compression
- Image optimization
- Lazy loading

## Monitoring & Logging

- Django logging configuration
- Error tracking (Sentry integration ready)
- Performance monitoring
- User analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details
