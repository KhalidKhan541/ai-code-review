# AI Code Review Platform

An AI-powered code review platform that provides comprehensive code analysis, security scanning, and improvement suggestions.

## Features

- **AI-Powered Analysis**: Get instant code reviews using advanced AI models
- **Security Scanning**: Detect vulnerabilities and security issues
- **Code Quality Scores**: Comprehensive scoring across multiple dimensions
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, Go, Rust, and more
- **Detailed Reports**: In-depth analysis with actionable recommendations
- **Team Collaboration**: Share and track code quality across teams

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Authentication**: JWT with bcrypt password hashing
- **AI Integration**: OpenAI GPT-4 / Anthropic Claude
- **Caching**: Redis
- **Testing**: pytest with 80%+ coverage

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **State Management**: React Query
- **Form Handling**: React Hook Form + Zod validation
- **Testing**: Jest + React Testing Library

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/KhalidKhan541/ai-code-review.git
cd ai-code-review
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
```

3. Set up the frontend:
```bash
cd frontend
npm install
cp .env.example .env
```

4. Start the development servers:
```bash
# Using Docker Compose (recommended)
docker compose up

# Or manually
# Terminal 1 - Backend
cd backend && uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

5. Open http://localhost:3000 in your browser.

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Backend Tests
```bash
cd backend
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm run test:coverage
```

## Project Structure

```
ai-code-review/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── security/      # Authentication & security
│   │   └── services/      # Business logic
│   ├── tests/             # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js app routes
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities & API client
│   │   └── types/         # TypeScript types
│   └── package.json
├── .github/workflows/     # CI/CD pipelines
└── docker-compose.yml     # Development environment
```

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
