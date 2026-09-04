# Deployment Guide

## Prerequisites

- Docker and Docker Compose
- Domain name (for production)
- SSL certificate (recommended)

## Quick Start (Development)

```bash
# Clone the repository
git clone https://github.com/KhalidKhan541/ai-code-review.git
cd ai-code-review

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start development servers
docker compose up
```

Access the application at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Production Deployment

### 1. Environment Variables

Create production `.env` files:

```bash
# backend/.env
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/ai_code_review
SECRET_KEY=your-production-secret-key
OPENAI_API_KEY=your-api-key
REDIS_URL=redis://redis:6379/0
CORS_ORIGINS=["https://yourdomain.com"]
DEBUG=false

# frontend/.env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api/v1
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=https://yourdomain.com
```

### 2. Docker Compose Production

```bash
docker compose -f docker-compose.prod.yml up -d
```

### 3. SSL Configuration

Add nginx with SSL termination:

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://frontend:3000;
    }

    location /api {
        proxy_pass http://backend:8000;
    }
}
```

### 4. Database Migration

```bash
# Run migrations
docker compose exec backend alembic upgrade head
```

## Monitoring

- Health check: `GET /health`
- Logs: `docker compose logs -f`
- Metrics: Add Prometheus/Grafana as needed

## Scaling

Use Docker Swarm or Kubernetes for horizontal scaling:

```bash
# Docker Swarm
docker swarm init
docker stack deploy -c docker-compose.prod.yml ai-code-review
```
