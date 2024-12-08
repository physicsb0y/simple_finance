# Simple Finance

# Project Setup Guide

## Prerequisites
- Python 3.8+
- Redis
- pip
- virtualenv

## Installation Steps

1. **Install Redis**
   ```bash
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install redis-server

   # For macOS
   brew install redis

   # For Windows
   # Download and install from Redis official website
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env file and fill in required variables
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## User Creation

### Option 1: Create Superuser
```bash
python manage.py createsuperuser
```

### Option 2: Create Normal User
- Navigate to `/accounts/api/user/` in your browser or via API client
- Fill out user registration form

## Authentication

1. Get Authentication Token
   - Visit `/accounts/api/token/`
   - Provide credentials
   - Receive JWT token for API access



NOTE: You can access the API documentation at `/api/schema/swagger-ui/`
