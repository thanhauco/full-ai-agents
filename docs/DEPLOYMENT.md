# Deployment Guide

## Production Deployment

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (optional)
- API keys for LLM providers
- PostgreSQL database
- Redis instance
- Pinecone account (for vector storage)

## Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t ai-agent-system:latest .

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f ai-agent

# Stop services
docker-compose down
```

### Environment Variables

Create a `.env` file with:

```bash
# LLM Providers
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:pass@postgres:5432/ai_agent

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Vector Database
PINECONE_API_KEY=your_key_here
PINECONE_ENVIRONMENT=your_env_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
JWT_SECRET_KEY=your_secret_key_here
```

## Kubernetes Deployment

### Create Namespace

```bash
kubectl create namespace ai-agent
```

### Deploy Services

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

### Check Status

```bash
kubectl get pods -n ai-agent
kubectl get services -n ai-agent
kubectl logs -f deployment/ai-agent -n ai-agent
```

## Monitoring

### Prometheus Metrics

Metrics are exposed at `/metrics` endpoint.

### Health Checks

- Liveness: `GET /health`
- Readiness: `GET /health`

## Scaling

### Horizontal Scaling

```bash
# Docker Compose
docker-compose up --scale ai-agent=3

# Kubernetes
kubectl scale deployment ai-agent --replicas=3 -n ai-agent
```

## Security

### SSL/TLS

Configure SSL certificates in your reverse proxy (nginx, traefik).

### API Authentication

JWT tokens are required for protected endpoints.

### Rate Limiting

Configured per user/IP in environment variables.

## Backup and Recovery

### Database Backup

```bash
docker-compose exec postgres pg_dump -U postgres ai_agent > backup.sql
```

### Restore

```bash
docker-compose exec -T postgres psql -U postgres ai_agent < backup.sql
```

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker-compose logs ai-agent
```

### Database Connection Issues

Verify DATABASE_URL and network connectivity.

### High Memory Usage

Adjust container memory limits in docker-compose.yml.

## Performance Tuning

- Enable Redis caching
- Adjust worker count
- Configure connection pooling
- Optimize database queries

## Maintenance

### Update Application

```bash
git pull
docker-compose build
docker-compose up -d
```

### Clean Up

```bash
docker system prune -a
docker volume prune
```
