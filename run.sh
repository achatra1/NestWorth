#!/bin/bash

# NestWorth Application Runner
# This script helps start the NestWorth API server

echo "🏡 NestWorth - Baby Budget Planner"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/installed" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
    echo "✅ Dependencies installed"
fi

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL connection..."
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running on localhost:5432"
    echo "   You can start it with: docker-compose up -d"
    echo "   Or update DATABASE_URL in .env to point to your database"
fi

# Initialize database if needed
echo "🗄️  Checking database..."
python init_db.py

echo ""
echo "🚀 Starting NestWorth API server..."
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
