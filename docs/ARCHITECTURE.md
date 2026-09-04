# Architecture Overview

## System Architecture

The AI Code Review Platform follows a modern full-stack architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend                           │
│                   (Next.js 14)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Pages     │  │ Components  │  │   Hooks     │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                         │                               │
│                    ┌────┴────┐                          │
│                    │ API Lib │                          │
│                    └────┬────┘                          │
└─────────────────────────┼───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                      Backend                            │
│                    (FastAPI)                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Routes    │  │  Services   │  │   Models    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                         │                               │
│  ┌──────────────────────┼──────────────────────┐       │
│  │                      │                      │       │
│  ▼                      ▼                      ▼       │
│ ┌──────────┐     ┌──────────┐           ┌──────────┐  │
│ │PostgreSQL│     │  Redis   │           │ AI APIs  │  │
│ └──────────┘     └──────────┘           └──────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Key Components

### Frontend
- **App Router**: File-based routing with server components
- **React Query**: Server state management
- **Tailwind CSS**: Utility-first styling
- **TypeScript**: Type safety throughout

### Backend
- **FastAPI**: High-performance async API framework
- **SQLAlchemy**: Async ORM for database operations
- **Pydantic**: Data validation and serialization
- **JWT**: Stateless authentication

### Database
- **PostgreSQL**: Primary data store
- **Redis**: Caching and rate limiting

### AI Integration
- **OpenAI/Anthropic**: Code analysis models
- **Prompt Engineering**: Optimized for code review
- **Response Parsing**: Structured output handling

## Data Flow

1. User submits code via frontend
2. Frontend sends request to backend API
3. Backend validates and stores submission
4. AI engine analyzes code
5. Results stored in database
6. Report returned to frontend
7. Frontend displays analysis results

## Security Architecture

- Authentication: JWT with refresh tokens
- Authorization: Role-based access control
- Input Validation: Pydantic schemas
- SQL Injection: Prevented via ORM
- Rate Limiting: Redis-backed limiter
- CORS: Configured per environment
