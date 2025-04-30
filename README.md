# Django REST API

A modular Django REST Framework project for managing employees, authentication, and leave requests, with role-based access control.

## Features

- **User Authentication** (JWT)
- **Employee Management** (Admin creates employees, auto-creates user accounts)
- **Leave Management** (Employees can request leaves, admins can approve/reject)
- **Role-Based Permissions** (Admin vs Employee)
- **Browsable API** (via DRF)

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
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

## API Overview

### Authentication

- `POST /api/token/` — Obtain JWT token
- `POST /api/token/refresh/` — Refresh JWT token

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

### Permissions

- **Admin**: Full access to all endpoints.
- **Employee**: Can only manage their own leaves, view leave types and approvals.

## Role-Based Access

- When an admin creates an employee, a user account is auto-created (password: `<surname>123`).
- Employees can only access their own leave data.
- Admins can access and manage all data.

## Version Control

The project includes a `.gitignore` file that excludes:
- Virtual environment files (`env/`)
- Python cache and compiled files
- Database files (`db.sqlite3`)
- Environment variable files (`.env`)
- IDE-specific files
- OS-specific files

## Testing

```bash
pytest
```

## Dependencies

- Django >= 4.2.0
- djangorestframework >= 3.14.0
- factory-boy >= 3.3.0
- pytest >= 7.4.0
- pytest-django >= 4.5.2

---

**For more details, see the code in each app's `views.py`, `serializers.py`, and `models.py`.** 