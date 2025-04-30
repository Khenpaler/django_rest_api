# Django REST API

A comprehensive Django REST Framework project that implements a complete employee management system with authentication, leave management, and role-based access control.

## Project Overview

This project demonstrates the implementation of a modern REST API using Django and Django REST Framework. It serves as a practical example of building a production-ready API with proper authentication, authorization, and business logic.

### Key Features

- **Secure Authentication**: JWT-based authentication system with token refresh capabilities
- **Employee Management**: Complete CRUD operations for employee records
- **Leave Management**: Comprehensive leave request and approval workflow
- **Role-Based Access Control**: Fine-grained permissions for different user roles
- **Browsable API**: Interactive API documentation and testing interface
- **Environment Configuration**: Secure handling of sensitive settings using environment variables

## What I Learned

Through building this project, I gained hands-on experience with:

1. **Django REST Framework**
   - Building RESTful APIs with proper endpoints
   - Implementing custom serializers and views
   - Handling different HTTP methods and status codes
   - Creating nested serializers for complex data structures

2. **Authentication & Authorization**
   - JWT token implementation
   - Custom user model creation
   - Role-based permission system
   - Secure password handling

3. **Database Design**
   - Creating models with proper relationships
   - Implementing custom model methods
   - Handling database migrations
   - Optimizing database queries

4. **Security Best Practices**
   - Environment variable management
   - Secure password handling
   - Input validation
   - CSRF protection
   - Rate limiting considerations

5. **Testing**
   - Writing unit tests
   - Using factory-boy for test data
   - Testing authentication flows
   - API endpoint testing

6. **Project Structure**
   - Modular application design
   - Separation of concerns
   - Reusable components
   - Configuration management

## Technologies Used

### Core Technologies
- **Django** (>=4.2.0) - The web framework for perfectionists with deadlines
- **Django REST Framework** (>=3.14.0) - Powerful and flexible toolkit for building Web APIs
- **Django REST Framework SimpleJWT** (>=5.3.0) - JSON Web Token authentication plugin

### Development Tools
- **Python** - Programming language
- **SQLite** - Database (can be configured for other databases)
- **python-dotenv** - Environment variable management
- **pytest** - Testing framework
- **factory-boy** - Test fixtures replacement

### API Features
- RESTful architecture
- JWT authentication
- Browsable API interface
- Nested serializers
- Custom permissions
- Query parameter filtering

## Project Structure

```
django_rest_api/
├── apps/
│   ├── authentication/   # Custom user model, login, registration
│   ├── employees/        # Employee CRUD, auto-user creation
│   └── leaves/           # Leave types, leave requests, approvals, permissions
├── django_rest_api/      # Project settings and URLs
├── manage.py
├── requirements.txt
├── .gitignore           # Git ignore rules for Python/Django projects
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd django_rest_api
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy `.env.example` to `.env` and configure your settings:
```bash
cp .env.example .env
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

## API Documentation

### Authentication

#### Token Management
- `POST /api/token/` — Obtain JWT token
- `POST /api/token/refresh/` — Refresh JWT token

#### User Authentication
- `POST /api/auth/register/` — Register a new user
- `POST /api/auth/login/` — Login and obtain JWT tokens
- `POST /api/auth/logout/` — Logout and invalidate refresh token
- `GET /api/auth/profile/` — Get current user profile
- `PUT /api/auth/profile/` — Update current user profile
- `PATCH /api/auth/profile/` — Partially update current user profile

### Employees

- `GET /api/employees/` — List employees (admin only)
- `POST /api/employees/` — Create employee (admin only, auto-creates user)
- `GET /api/employees/{id}/` — Retrieve employee

### Leaves

- `GET /api/leave_types/` — List leave types
- `GET /api/leaves/` — List leaves (employee: own, admin: all)
- `POST /api/leaves/` — Create leave request (employee or admin)
- `GET /api/leave_approvals/` — List leave approvals (employee: own, admin: all)
- `POST /api/leave_approvals/` — Approve leave (admin only)

## Testing

Run the test suite:
```bash
pytest
```

## Security Considerations

- All sensitive settings are managed through environment variables
- JWT tokens are used for authentication
- Role-based access control is implemented
- Input validation is performed at multiple levels
- Database queries are protected against SQL injection
- CSRF protection is enabled

## Future Improvements

- Add API documentation using Swagger/OpenAPI
- Implement rate limiting
- Add more comprehensive test coverage
- Implement caching for frequently accessed data
- Add support for file uploads
- Implement email notifications
- Add audit logging
- Support for multiple database backends

---

**For more details, see the code in each app's `views.py`, `serializers.py`, and `models.py`.** 