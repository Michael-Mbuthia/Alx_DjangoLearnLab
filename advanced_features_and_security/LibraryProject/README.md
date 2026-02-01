# LibraryProject README

## Overview
LibraryProject is a Django-based library management application that allows users to manage books, members, and borrowing records.

## Features
- Book catalog management
- Member registration and management
- Borrowing and returning system
- Search and filter functionality
- Admin dashboard

## Installation

### Prerequisites
- Python 3.8+
- Django 3.2+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/Michael-Mbuthia/Introduction_to_Django.git

# Navigate to project directory
cd LibraryProject

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Usage
Access the application at `http://localhost:8000`

## Security & HTTPS (Production Notes)

This project includes several security hardening measures in
[advanced_features_and_security/LibraryProject/LibraryProject/settings.py](advanced_features_and_security/LibraryProject/LibraryProject/settings.py).

### HTTPS enforcement
- `SECURE_SSL_REDIRECT=True`: redirects all HTTP requests to HTTPS.
- HSTS enabled:
    - `SECURE_HSTS_SECONDS=31536000` (1 year)
    - `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
    - `SECURE_HSTS_PRELOAD=True`

If you terminate TLS at a reverse proxy/load balancer, enable:
- `DJANGO_SECURE_PROXY_SSL_HEADER=True` (requires proxy sends `X-Forwarded-Proto: https`).

### Secure cookies
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`

### Browser protections
- `X_FRAME_OPTIONS='DENY'` (clickjacking protection)
- `SECURE_CONTENT_TYPE_NOSNIFF=True`
- `SECURE_BROWSER_XSS_FILTER=True` (legacy browser protection)

### Content Security Policy (CSP)
`django-csp` is enabled via middleware and a baseline CSP is configured:
- Default allows only self-hosted resources.
- Inline styles are allowed (`'unsafe-inline'`) because templates use inline `<style>` blocks.
- Inline scripts are not allowed by default.

### Permissions & groups
Custom Book permissions are defined with codenames:
- `can_view`, `can_create`, `can_edit`, `can_delete`

Default groups are created after migrations:
- `Viewers`, `Editors`, `Admins` (see [advanced_features_and_security/LibraryProject/bookshelf/signals.py](advanced_features_and_security/LibraryProject/bookshelf/signals.py)).

### Required production environment variables
- `DJANGO_SECRET_KEY`: strong random secret key
- `DJANGO_ALLOWED_HOSTS`: comma-separated hosts (e.g. `example.com,www.example.com`)

Optional toggles:
- `DJANGO_DEBUG=True` (development only)
- `DJANGO_SECURE_SSL_REDIRECT=False` (development over HTTP)
- `DJANGO_SECURE_HSTS_SECONDS=0` (development)

## Project Structure
```
LibraryProject/
├── manage.py
├── requirements.txt
├── LibraryProject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── library/
    ├── models.py
    ├── views.py
    └── templates/
```

## Contributing
Pull requests are welcome. Please follow PEP 8 style guidelines.

## License
MIT License