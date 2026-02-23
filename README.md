# KILIMO GURU - Smart Agriculture Platform for Kenya

A comprehensive web-based agricultural management system designed specifically for Kenyan farmers. KILIMO GURU provides tools for crop management, market access, weather forecasting, M-Pesa integration, and expert advisory services.

## Features

### Core Features

1. **Farmer Registry & Profiles**
   - Digital signup with KIAMIS integration
   - Farm mapping via GPS
   - Soil and crop history tracking
   - Credit scoring for loans

2. **Weather & Climate Alerts**
   - Real-time weather forecasts
   - Drought and flood warnings
   - Irrigation advice
   - SMS/USSD notifications

3. **Crop & Livestock Management**
   - Planting calendars for Kenyan regions
   - AI-powered pest/disease detection
   - Yield tracking
   - Crop rotation planning
   - Livestock management

4. **Marketplace & Price Transparency**
   - Produce listings
   - Buyer matching
   - Real-time prices from major markets
   - Direct M-Pesa payments

5. **Input e-Commerce**
   - Verified seeds and fertilizers
   - Agro-vet locator
   - Delivery services

6. **Finance Tools**
   - M-Pesa integration
   - Farm loans and credit
   - Crop insurance
   - Credit scoring

7. **Advisory & E-Learning**
   - Expert articles and videos
   - Webinars
   - One-on-one consultations
   - Tele-veterinary services
   - Content in Swahili and local languages

8. **Analytics Dashboard**
   - Yield forecasts
   - Profitability reports
   - Market trends
   - Farm performance metrics

9. **Offline Mode & PWA**
   - Works without internet
   - Data sync when connected
   - Mobile app-like experience

## Technology Stack

- **Backend**: Django 4.2+
- **Frontend**: Tailwind CSS, Vanilla JavaScript
- **Database**: PostgreSQL (production), SQLite (development)
- **Cache**: Redis
- **Task Queue**: Celery
- **API**: Django REST Framework

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL (optional, SQLite works for development)
- Redis (optional, for caching and Celery)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kilimo-guru.git
cd kilimo-guru
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Load initial data (optional):
```bash
python manage.py loaddata fixtures/initial_data.json
```

8. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to access the application.

## API Documentation

The API is available at `/api/` and provides endpoints for:

- Crops: `/api/crops/`
- Produce Listings: `/api/produce/`
- Weather Data: `/api/weather/`
- Farmer Profile: `/api/farmer/profile/`
- Market Prices: `/api/market/prices/`

## M-Pesa Integration

To enable M-Pesa payments:

1. Register at [Safaricom Developer Portal](https://developer.safaricom.co.ke/)
2. Create an app and get your credentials
3. Add credentials to your `.env` file
4. Configure the callback URL in your Safaricom app

## SMS Integration

To enable SMS notifications:

1. Register at [Africa's Talking](https://africastalking.com/)
2. Get your API key
3. Add credentials to your `.env` file

## Deployment

### Using Gunicorn

```bash
gunicorn kilimo_guru.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

```bash
docker-compose up -d
```

### Environment Variables for Production

Make sure to set these in production:

- `DEBUG=False`
- `SECRET_KEY` - Generate a strong random key
- `ALLOWED_HOSTS` - Your domain names
- Database credentials
- All API keys for external services

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@kilimoguru.co.ke or call +254 700 000 000.

## Acknowledgments

- Kenya Agricultural and Livestock Research Organization (KALRO)
- Kenya Meteorological Department (KMD)
- Agriculture and Food Authority (AFA)
- Kenya National Farmers Federation (KENAFF)
