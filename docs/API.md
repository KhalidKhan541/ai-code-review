# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All protected endpoints require a Bearer token:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "Full Name"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response** (200 OK):
```json
{
  "access_token": "jwt-token",
  "refresh_token": "jwt-refresh-token",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```

### Code Analysis

#### Create Analysis
```http
POST /analysis/
Authorization: Bearer <token>
Content-Type: application/json

{
  "code_content": "def hello():\n    print('Hello')",
  "language": "python",
  "file_name": "hello.py"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid",
  "status": "completed",
  "language": "python",
  "file_name": "hello.py",
  "overall_score": 85,
  "grade": "B+",
  "scores": {
    "test_coverage": 80,
    "dependency_health": 90,
    "code_cleanliness": 85,
    "architecture": 85,
    "security": 85
  },
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### List Analyses
```http
GET /analysis/?page=1&per_page=10
Authorization: Bearer <token>
```

#### Get Analysis
```http
GET /analysis/{analysis_id}
Authorization: Bearer <token>
```

### Reports

#### Get Report
```http
GET /reports/{analysis_id}
Authorization: Bearer <token>
```

#### Get Issues
```http
GET /reports/{analysis_id}/issues
Authorization: Bearer <token>
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 429 Rate Limited
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```
