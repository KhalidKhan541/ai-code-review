# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email: khalidkhan46572@gmail.com
3. Include detailed steps to reproduce
4. Allow reasonable time for response

## Security Measures

### Authentication
- JWT tokens with expiration
- Bcrypt password hashing
- Secure token storage on client side

### API Security
- Rate limiting on all endpoints
- Input validation and sanitization
- CORS configuration
- SQL injection prevention via ORM

### Data Security
- Environment variables for secrets
- No hardcoded credentials
- Encrypted sensitive data

## Scope

This security policy applies to:
- Backend API (FastAPI)
- Frontend application (Next.js)
- Database queries
- Authentication system

## Updates

We regularly update dependencies to patch security vulnerabilities. Run:
```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm update
```

Thank you for helping keep this project secure!
