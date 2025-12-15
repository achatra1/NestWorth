.PHONY: help build up down restart logs shell test clean

# Default target
help:
	@echo "🏡 NestWorth - Docker Management Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make restart  - Restart all services"
	@echo "  make logs     - View logs (follow mode)"
	@echo "  make shell    - Open shell in API container"
	@echo "  make test     - Run tests in container"
	@echo "  make clean    - Stop and remove all containers, networks, and volumes"
	@echo "  make rebuild  - Clean rebuild (fresh start)"
	@echo ""

# Build Docker images
build:
	@echo "🔨 Building Docker images..."
	docker-compose build

# Start all services
up:
	@echo "🚀 Starting NestWorth services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "   API: http://localhost:8000"
	@echo "   Docs: http://localhost:8000/docs"

# Start with logs visible
up-logs:
	@echo "🚀 Starting NestWorth services (with logs)..."
	docker-compose up

# Stop all services
down:
	@echo "🛑 Stopping services..."
	docker-compose down

# Restart services
restart:
	@echo "🔄 Restarting services..."
	docker-compose restart

# View logs
logs:
	docker-compose logs -f

# Open shell in API container
shell:
	docker-compose exec nestworth-api bash

# Run tests
test:
	@echo "🧪 Running tests..."
	docker-compose exec nestworth-api pytest -v

# Clean everything
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	@echo "✅ Cleanup complete!"

# Rebuild everything from scratch
rebuild: clean
	@echo "🔨 Rebuilding everything..."
	docker-compose up --build -d
	@echo "✅ Rebuild complete!"
	@echo "   API: http://localhost:8000"
	@echo "   Docs: http://localhost:8000/docs"

# Check status
status:
	@echo "📊 Service status:"
	docker-compose ps

# Health check
health:
	@echo "🏥 Checking API health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ API not responding"
