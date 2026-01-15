
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
