# 🚀 Finance Tracking Backend System

> A **production-ready**, enterprise-grade REST API for comprehensive financial record management, built with **FastAPI**, **SQLAlchemy**, and **JWT authentication**. Features advanced analytics, role-based access control, and professional API documentation.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌐 Live Demo
Access the live API documentation here:

[https://finance-tracking-backend.onrender.com/docs](https://finance-tracking-backend.onrender.com/docs)

---

## 📋 Table of Contents

- [Live Demo](#-live-demo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Render Deployment](#-render-deployment)
- [API Documentation](#-api-documentation)
- [Role-Based Access Control](#-role-based-access-control)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Security](#-security)
- [Performance Optimizations](#-performance-optimizations)
- [Contributing](#-contributing)

---

## ✨ Features

### 🔐 **Authentication & Security**
- JWT-based authentication with 24-hour token expiry
- Bcrypt password hashing
- Role-based access control (RBAC)
- Secure API endpoints with proper HTTP status codes

### 💰 **Financial Management**
- Complete CRUD operations for transactions
- Advanced filtering (date range, category, type)
- Pagination support (configurable page sizes)
- Input validation with detailed error messages

### 📊 **Analytics & Insights**
- Real-time financial overview (income, expenses, balance)
- Category-wise spending analysis
- Monthly financial breakdowns
- Recent transaction history

### 👥 **User Management**
- Multi-role system (Viewer, Analyst, Admin)
- User registration and authentication
- Admin-only user role management
- Secure user data handling

### 🛠 **Developer Experience**
- Auto-generated Swagger UI documentation
- Interactive API testing interface
- Comprehensive unit test suite
- Professional logging system
- Type hints throughout codebase

---

## � Why I Built This Project

This project demonstrates **enterprise-grade backend system design** for a financial tracking application, showcasing modern Python development practices and production-ready architecture.

### **Key Learning Objectives**
- **Clean Architecture**: Modular design with clear separation of concerns (routers, services, models, schemas)
- **Secure Authentication**: Implementation of JWT-based authentication with bcrypt password hashing
- **Role-Based Access Control**: Multi-level permission system ensuring data security and proper access management
- **Data Analytics**: Efficient query optimization and aggregation for financial insights
- **Scalable API Design**: RESTful endpoints with proper HTTP status codes, validation, and documentation

### **Real-World Application**
This system could serve as the backend for personal finance apps, business expense trackers, or financial management tools, handling user authentication, transaction management, and analytical reporting with enterprise-level security and performance.

---

## 🔒 Security Features

### **Environment Variable Configuration**
- Sensitive configuration (JWT secrets, database URLs) loaded from `.env` files
- No hardcoded secrets in source code
- Production-ready configuration management

### **Password Security**
- bcrypt hashing for all passwords
- Secure password verification with timing attack protection
- Minimum password length requirements

### **Authentication & Authorization**
- JWT bearer token authentication
- Configurable token expiration (30 minutes default)
- Role-based access control (Viewer/Analyst/Admin)
- Clear permission error messages

### **Rate Limiting**
- Login endpoint protected against brute-force attacks
- Maximum 5 attempts per minute per username
- HTTP 429 responses for rate limit violations

---

## 🌍 Real-World Considerations

### **Production Deployment**
- Environment-based configuration for different deployment stages
- Proper error handling and logging for monitoring
- Database connection pooling and optimization
- API rate limiting to prevent abuse

### **Security Best Practices**
- Prevention of brute-force login attacks through rate limiting
- Protection of sensitive configuration data
- Secure password storage and verification
- Role-based data access control

### **Scalability & Performance**
- Efficient database queries with proper indexing
- Modular architecture for easy feature extension
- Comprehensive testing for reliability
- Professional logging for debugging and monitoring

---

## �🛠 Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Framework** | FastAPI | 0.135.3 |
| **Database** | SQLite + SQLAlchemy | 2.0.48 |
| **Authentication** | JWT (python-jose) | 3.5.0 |
| **Password Hashing** | bcrypt | 5.0.0 |
| **Validation** | Pydantic | 2.12.5 |
| **Testing** | pytest | 9.0.2 |
| **ASGI Server** | Uvicorn | 0.42.0 |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** installed
- **pip** package manager

### 1. Clone & Setup
```bash
# Navigate to project directory
cd finance_system/

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application Locally
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the Application
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### 4. Test the API
1. Open http://localhost:8000/docs
2. Use seed credentials to login
3. Click "Authorize" and paste the JWT token
4. Explore all endpoints interactively

---

## ☁️ Render Deployment

This project is ready to deploy on Render.

### Required files
- `requirements.txt`
- `start.sh`
- `runtime.txt`

### start.sh content
```bash
#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### runtime.txt content
```text
python-3.13.0
```

### Build and start commands for Render
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `bash start.sh`

### Environment variables in Render
Add these values under the Render Web Service "Environment" section:
- `SECRET_KEY` = a secure random JWT secret
- `ALGORITHM` = `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`
- `DATABASE_URL` = `sqlite:///./finance.db` (or use PostgreSQL for production)

### GitHub preparation
```bash
git add .
git commit -m "deployment setup"
git push origin main
```

### Deploying on Render
1. Go to [render.com](https://render.com) and create a new Web Service.
2. Connect your GitHub repo.
3. Use the following values:
   - Name: `finance-tracking-backend`
   - Runtime: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `bash start.sh`
4. Add the required environment variables.
5. Click **Manual Deploy** to deploy the latest commit.

### Verify deployment
- Open: `https://finance-tracking-backend.onrender.com/docs`
- Expected result: FastAPI Swagger UI should appear

### Important production note
This repo uses SQLite by default. On Render, SQLite file storage is ephemeral and may reset after deployments. For production, use PostgreSQL and set `DATABASE_URL` to the Render PostgreSQL URL.

---

## 🔐 Role-Based Access Control

### User Roles & Permissions

| Role | Description | Permissions |
|------|-------------|-------------|
| **Viewer** | Read-only access | ✅ View transactions<br>✅ View personal analytics<br>❌ Create/Update/Delete |
| **Analyst** | Analysis access | ✅ All Viewer permissions<br>✅ Advanced filtering<br>✅ Category analytics<br>✅ Monthly reports |
| **Admin** | Full access | ✅ All Analyst permissions<br>✅ CRUD operations<br>✅ User management |

### Seed Users for Testing

| Username | Password | Role | Description |
|----------|----------|------|-------------|
| `admin_user` | `admin123` | Admin | Full system access |
| `analyst_user` | `analyst123` | Analyst | Analytics & filtering |
| `viewer_user` | `viewer123` | Viewer | Read-only access |

### Access Control Examples

```bash
# ✅ Viewer can access
GET /transactions
GET /summary/overview
GET /summary/recent

# ❌ Viewer cannot access (403 Forbidden)
POST /transactions
GET /summary/by-category
PUT /users/1

# ✅ Analyst can access
GET /summary/by-category
GET /summary/monthly

# ✅ Admin can access everything
POST /transactions
DELETE /transactions/1
GET /users
PUT /users/1
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/register` | Register new user | ❌ No |
| `POST` | `/auth/login` | Login & get JWT | ❌ No |

### Transactions (CRUD)
| Method | Endpoint | Description | Roles |
|--------|----------|-------------|-------|
| `GET` | `/transactions` | List with filtering/pagination | viewer, analyst, admin |
| `POST` | `/transactions` | Create transaction | admin |
| `GET` | `/transactions/{id}` | Get single transaction | viewer, analyst, admin |
| `PUT` | `/transactions/{id}` | Update transaction | admin |
| `DELETE` | `/transactions/{id}` | Delete transaction | admin |

### Analytics
| Method | Endpoint | Description | Roles |
|--------|----------|-------------|-------|
| `GET` | `/summary/overview` | Financial overview | viewer, analyst, admin |
| `GET` | `/summary/by-category` | Category breakdown | analyst, admin |
| `GET` | `/summary/monthly` | Monthly analysis | analyst, admin |
| `GET` | `/summary/recent` | Recent transactions | viewer, analyst, admin |

### User Management
| Method | Endpoint | Description | Roles |
|--------|----------|-------------|-------|
| `GET` | `/users` | List all users | admin |
| `GET` | `/users/{id}` | Get user details | admin |
| `PUT` | `/users/{id}` | Update user role | admin |

### Health Check
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/` | API health status | ❌ No |

---

## 🧪 Testing

### Run Unit Tests
```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=finance_system --cov-report=html
```

### Test Results
```
======================== 5 passed in 2.96s ========================
tests/test_auth_service.py::test_hash_password PASSED
tests/test_auth_service.py::test_verify_password PASSED
tests/test_auth_service.py::test_create_and_decode_token PASSED
tests/test_auth_service.py::test_decode_invalid_token PASSED
tests/test_summary_service.py::test_get_overview PASSED
```

### Manual API Testing
1. Start the server: `uvicorn main:app --reload`
2. Open http://localhost:8000/docs
3. Test authentication flow
4. Verify role-based restrictions
5. Test CRUD operations

---

## 🏗 Project Structure

```
finance_system/
├── main.py                 # FastAPI app factory & startup logic
├── config.py               # Application configuration
├── database.py             # SQLAlchemy engine & session
├── dependencies.py         # FastAPI dependencies (auth, RBAC)
├── requirements.txt        # Python dependencies
│
├── models/                 # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py            # User model with indexes
│   └── transaction.py     # Transaction model with indexes
│
├── schemas/                # Pydantic schemas & validation
│   ├── __init__.py
│   ├── user.py            # User request/response schemas
│   └── transaction.py     # Transaction & analytics schemas
│
├── routers/                # API route handlers
│   ├── __init__.py
│   ├── auth.py            # Authentication endpoints
│   ├── transactions.py    # CRUD operations
│   ├── summary.py         # Analytics endpoints
│   └── users.py           # User management
│
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── auth_service.py    # JWT & password handling
│   └── summary_service.py # Analytics calculations
│
└── tests/                  # Unit test suite
    ├── __init__.py
    ├── conftest.py        # Test fixtures
    ├── test_auth_service.py
    ├── test_summary_service.py
    └── finance_system.log # Application logs
```

---

## 🗄 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR DEFAULT 'viewer' NOT NULL,
    created_at DATETIME
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    amount FLOAT NOT NULL,
    type VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    date DATE NOT NULL,
    notes VARCHAR,
    created_at DATETIME
);

-- Performance indexes
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_user_date ON transactions(user_id, date);
CREATE INDEX idx_transactions_type_category ON transactions(type, category);
```

---

## 🔒 Security

### Authentication
- **JWT Tokens**: Bearer token authentication
- **Token Expiry**: 24 hours default
- **Password Security**: bcrypt hashing with salt

### Authorization
- **Role-Based Access**: Viewer, Analyst, Admin
- **Endpoint Protection**: Automatic RBAC enforcement
- **Error Handling**: Clear 401/403 responses

### Data Protection
- **Input Validation**: Pydantic schemas
- **SQL Injection Prevention**: SQLAlchemy ORM
- **Secure Defaults**: No sensitive data in logs

---

## ⚡ Performance Optimizations

### Database Indexes
- **user_id**: Foreign key lookups
- **date**: Date range filtering
- **Composite indexes**: Multi-column queries
- **Primary keys**: Automatic indexing

### Query Optimization
- **Selective loading**: Only fetch required data
- **Pagination**: Prevent large result sets
- **Efficient aggregation**: Optimized summary queries

### Caching Strategy
- **Connection pooling**: SQLAlchemy session management
- **Prepared statements**: Query plan reuse

---

## 📖 API Usage Examples

### 1. Authentication Flow
```bash
# Register new user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "email": "john@example.com", "password": "secure123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin_user&password=admin123"
```

### 2. Transaction Management
```bash
# Get transactions (with auth token)
curl -X GET "http://localhost:8000/transactions?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Create transaction (admin only)
curl -X POST "http://localhost:8000/transactions" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000.0,
    "type": "income",
    "category": "freelance",
    "date": "2024-01-15",
    "notes": "Web development project"
  }'
```

### 3. Analytics
```bash
# Financial overview
curl -X GET "http://localhost:8000/summary/overview" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Monthly breakdown
curl -X GET "http://localhost:8000/summary/monthly?year=2024" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🎯 Why I Built This Project

This project demonstrates **backend system design for a financial tracking application**, showcasing production-ready practices that are essential for modern web development. It serves as a comprehensive example of how to build scalable, secure, and maintainable REST APIs using Python's most powerful tools.

### Key Design Principles Demonstrated

* **Clean Architecture**: Modular structure with clear separation of concerns (routers, services, models, schemas)
* **Secure Authentication**: JWT-based auth with bcrypt password hashing and role-based access control
* **Data Analytics**: Efficient aggregation queries and real-time financial insights
* **Scalable API Design**: RESTful endpoints with proper HTTP methods, status codes, and pagination
* **Production Readiness**: Environment configuration, logging, error handling, and comprehensive testing

### Learning Outcomes
- Implementing enterprise-grade security practices
- Designing APIs that scale with user growth
- Optimizing database queries for performance
- Writing maintainable, testable code
- Understanding real-world deployment considerations

---

## 🔐 Security Features

### Environment-Based Configuration
- **Sensitive data protection**: JWT secrets, algorithms, and timeouts loaded from `.env` files
- **No hardcoded secrets**: All configuration externalized for different environments
- **Secure defaults**: Production-safe settings with environment overrides

### Password Security
- **bcrypt hashing**: Industry-standard password hashing with salt
- **Secure verification**: Constant-time comparison to prevent timing attacks
- **Minimum requirements**: Enforced password complexity rules

### Authentication & Authorization
- **JWT tokens**: Stateless authentication with configurable expiry
- **Role-based access control**: Granular permissions (Viewer/Analyst/Admin)
- **Request validation**: Comprehensive input sanitization and validation

### Attack Prevention
- **Rate limiting**: Brute-force protection on login endpoints (5 attempts/minute per IP)
- **SQL injection prevention**: ORM-based queries with parameterized statements
- **XSS protection**: Proper content-type handling and input validation

---

## 🌐 Real-World Considerations

### Scalability
- **Database optimization**: Strategic indexes on frequently queried columns
- **Query efficiency**: Pagination and selective loading to handle large datasets
- **Connection pooling**: SQLAlchemy session management for concurrent requests

### Security Hardening
- **Brute-force mitigation**: Rate limiting prevents automated attack attempts
- **Configuration security**: Environment variables protect sensitive settings
- **Error handling**: No sensitive information leaked in error responses

### Production Deployment
- **Environment configuration**: Separate settings for dev/staging/production
- **Logging infrastructure**: Structured logging for monitoring and debugging
- **Health checks**: API status endpoints for load balancer monitoring

### Maintainability
- **Modular design**: Easy to extend with new features
- **Comprehensive testing**: Unit tests ensure reliability
- **Documentation**: Auto-generated API docs with examples

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Run tests**: `pytest tests/ -v`
4. **Commit changes**: `git commit -m 'Add amazing feature'`
5. **Push** to branch: `git push origin feature/amazing-feature`
6. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation
- Ensure all tests pass
- Use type hints consistently

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Powerful ORM toolkit
- **Pydantic** - Data validation library
- **JWT** - JSON Web Token implementation

---

**Built with ❤️ for demonstrating enterprise-grade Python backend development**
# finance-tracking-backend
