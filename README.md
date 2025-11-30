# Dynamic Form Builder - Backend

Django REST API for dynamic form schema, validation, and submissions management.

##  Tech Stack

- Django 5.0.1
- Django REST Framework
- django-cors-headers
- SQLite (Development)
- Python 3.8+

##  Project Structure
backend/
├── backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── forms_api/
│   ├── models.py
│   ├── serializers.py
│   ├── validators.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── db.sqlite3

##  Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Installation Steps

1. **Navigate to backend directory:**
```bash
   cd backend
```

2. **Create virtual environment:**
```bash
   python -m venv venv
   
   # Activate on Windows:
   venv\Scripts\activate
   
   # Activate on macOS/Linux:
   source venv/bin/activate
```

3. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

4. **Run migrations:**
```bash
   python manage.py makemigrations
   python manage.py migrate
```

5. **Create superuser (optional):**
```bash
   python manage.py createsuperuser
```
   **Use the following credentials:**
   - Username: `Prashant`
   - Email: `prashant10gpt@gmail.com` 
   - Password: `Prashant`

6. **Start development server:**
```bash
   python manage.py runserver
```

   Server runs on: `http://localhost:8000`

##  Features

- **Dynamic Form Schema** - Employee Onboarding form
- **Comprehensive Validation** - Server-side validation for all field types
- **RESTful API** - Clean API design with proper status codes
- **Pagination & Sorting** - Efficient data retrieval
- **CORS Enabled** - Frontend integration ready

##  API Endpoints

### 1. Get Form Schema
```http
GET /api/form-schema
```
**Response:** Form schema with fields, validation rules, and options

### 2. Submit Form
```http
POST /api/submissions
Content-Type: application/json

{
  "fullName": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "department": "engineering",
  "skills": ["javascript", "react"],
  "startDate": "2024-01-15",
  "bio": "Software engineer",
  "agreeToTerms": true
}
```
**Success Response (201):**
```json
{
  "success": true,
  "id": "uuid",
  "createdAt": "2024-11-30T10:30:00Z"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "errors": {
    "email": "Please enter a valid email address"
  }
}
```

### 3. Get Submissions
```http
GET /api/submissions?page=1&limit=10&sortBy=createdAt&sortOrder=desc
```
**Response:**
```json
{
  "submissions": [...],
  "total": 100,
  "page": 1,
  "limit": 10,
  "totalPages": 10
}
```

##  Configuration

### CORS Settings
Update `backend/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

### Database
Default: SQLite (`db.sqlite3`)

For production, configure PostgreSQL in `settings.py`.

##  Dependencies
Django==5.0.1
djangorestframework==3.14.0
django-cors-headers==4.3.1
python-dateutil==2.8.2

##  Testing API

### Using curl:
```bash
# Get form schema
curl http://localhost:8000/api/form-schema

# Get submissions
curl http://localhost:8000/api/submissions?page=1&limit=10

# Submit form (replace data with actual values)
curl -X POST http://localhost:8000/api/submissions \
  -H "Content-Type: application/json" \
  -d '{"fullName":"John Doe",...}'
```

### Using Browser:
- Schema: http://localhost:8000/api/form-schema
- Submissions: http://localhost:8000/api/submissions
- Admin Panel: http://localhost:8000/admin

##  Validation Rules

The form includes comprehensive validation:
- **Full Name:** Required, 2-100 characters
- **Email:** Required, valid email regex
- **Age:** Required, 18-100 range
- **Department:** Required, one of 5 options
- **Skills:** Required, 1-4 selections
- **Start Date:** Required, after 2024-01-01
- **Bio:** Optional, max 500 characters
- **Terms:** Required boolean

##  Troubleshooting

**Migration Errors:**
```bash
# Delete db.sqlite3 and migrations, then:
python manage.py makemigrations
python manage.py migrate
```

**Port Already in Use:**
```bash
python manage.py runserver 8001
```

**Module Not Found:**
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

##  Security Notes

For production deployment:
- Set `DEBUG = False`
- Change `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Use PostgreSQL
- Enable HTTPS
- Use environment variables