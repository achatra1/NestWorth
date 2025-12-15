# 🐳 NestWorth Docker Guide

Complete guide for running NestWorth in Docker containers.

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

**Start everything with one command:**

```bash
docker-compose up --build
```

This will:
- Build the NestWorth API container
- Start PostgreSQL database
- Initialize database tables automatically
- Start the API on http://localhost:8000

**Access the application:**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Demo Blueprint: Try POST /blueprint in the docs

**Stop the application:**
```bash
docker-compose down
```

**Stop and remove all data:**
```bash
docker-compose down -v
```

---

## 🔧 Option 2: Build and Run Individual Container

### Build the Docker Image

```bash
docker build -t nestworth:latest .
```

### Run with Docker (standalone - no database)

```bash
docker run -p 8000:8000 nestworth:latest
```

The API will run but database operations will fail (demo endpoints still work).

### Run with External PostgreSQL

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg2://user:pass@host:5432/dbname" \
  nestworth:latest
```

---

## 📦 What's Included in the Container

- **Python 3.11** - Runtime environment
- **FastAPI** - Web framework
- **PostgreSQL client libraries** - Database connectivity
- **WeasyPrint** - PDF generation (with all dependencies)
- **All NestWorth code** - Complete application
- **Automatic database initialization** - Tables created on startup

---

## 🗂️ Docker Compose Services

### `nestworth-api`
- **Port**: 8000 (mapped to host:8000)
- **Container name**: nestworth-api
- **Dependencies**: postgres (waits for health check)
- **Volumes**: ./pdfs (for generated PDF reports)
- **Auto-restart**: yes

### `postgres`
- **Port**: 5432 (mapped to host:5432)
- **Container name**: nestworth-postgres
- **Database**: nestworth
- **User**: nestworth
- **Password**: nestworth123
- **Volume**: postgres_data (persistent storage)

---

## 🔍 Container Management

### View Logs

```bash
# All services
docker-compose logs -f

# Just the API
docker-compose logs -f nestworth-api

# Just PostgreSQL
docker-compose logs -f postgres
```

### Check Status

```bash
docker-compose ps
```

### Restart Services

```bash
# Restart everything
docker-compose restart

# Restart just the API
docker-compose restart nestworth-api
```

### Execute Commands in Container

```bash
# Open shell in API container
docker-compose exec nestworth-api bash

# Run tests in container
docker-compose exec nestworth-api pytest

# Check Python version
docker-compose exec nestworth-api python --version

# Initialize database manually
docker-compose exec nestworth-api python init_db.py
```

---

## 📊 Database Access

### Access PostgreSQL from Host

```bash
psql -h localhost -U nestworth -d nestworth
# Password: nestworth123
```

### Access PostgreSQL from Container

```bash
docker-compose exec postgres psql -U nestworth -d nestworth
```

### Backup Database

```bash
docker-compose exec postgres pg_dump -U nestworth nestworth > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker-compose exec -T postgres psql -U nestworth -d nestworth
```

---

## 🛠️ Development with Docker

### Mount Code for Live Reload

Edit `docker-compose.yml` to add volume mount:

```yaml
nestworth-api:
  volumes:
    - ./pdfs:/app/pdfs
    - ./apps:/app/apps        # Add this
    - ./packages:/app/packages # Add this
```

Then run with reload:

```bash
docker-compose up
```

Changes to code will auto-reload the server.

---

## 🔐 Environment Variables

You can customize these in `docker-compose.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | postgresql+psycopg2://... | Database connection string |
| `ENVIRONMENT` | production | Environment name |
| `PYTHONUNBUFFERED` | 1 | Disable Python buffering |
| `PYTHONPATH` | /app | Python module path |

---

## 📝 Production Deployment

### Build for Production

```bash
docker build -t nestworth:v1.0.0 .
```

### Tag and Push to Registry

```bash
# Tag for Docker Hub
docker tag nestworth:v1.0.0 yourusername/nestworth:v1.0.0

# Push to registry
docker push yourusername/nestworth:v1.0.0
```

### Run in Production

```bash
docker run -d \
  --name nestworth \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg2://..." \
  -e ENVIRONMENT=production \
  -v /var/nestworth/pdfs:/app/pdfs \
  --restart unless-stopped \
  nestworth:v1.0.0
```

---

## 🧪 Testing in Docker

### Run Tests

```bash
# Run all tests
docker-compose exec nestworth-api pytest

# Run with verbose output
docker-compose exec nestworth-api pytest -v

# Run specific test file
docker-compose exec nestworth-api pytest packages/tests/test_calculators_unit.py
```

---

## 🐛 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs nestworth-api

# Check if PostgreSQL is ready
docker-compose logs postgres
```

### Database connection errors

```bash
# Verify PostgreSQL is running
docker-compose ps postgres

# Check database health
docker-compose exec postgres pg_isready -U nestworth
```

### Port already in use

```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

### Clear everything and start fresh

```bash
# Stop and remove all containers, networks, volumes
docker-compose down -v

# Remove the built image
docker rmi nestworth:latest

# Rebuild and start
docker-compose up --build
```

---

## 📏 Container Size

Approximate sizes:
- **Base image** (python:3.11-slim): ~150 MB
- **With dependencies**: ~450 MB
- **Final image**: ~500 MB

---

## ⚡ Performance Tips

1. **Use volumes for development** - Mount code for faster iteration
2. **Multi-stage builds** - Reduce final image size (already optimized)
3. **Layer caching** - Requirements installed before code copy
4. **Health checks** - Ensure service availability
5. **Resource limits** - Add to docker-compose.yml if needed:

```yaml
nestworth-api:
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 512M
```

---

## 🔗 Useful Commands Cheat Sheet

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Rebuild
docker-compose up --build

# View logs
docker-compose logs -f

# Shell access
docker-compose exec nestworth-api bash

# Run tests
docker-compose exec nestworth-api pytest

# Check health
curl http://localhost:8000/health

# Fresh start
docker-compose down -v && docker-compose up --build
```

---

**Ready to deploy! 🚀**
