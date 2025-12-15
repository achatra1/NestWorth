#!/bin/bash
set -e

echo "🏡 NestWorth - Starting application..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if python -c "
import psycopg2
import os
try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL').replace('postgresql+psycopg2://', 'postgresql://'))
    conn.close()
    exit(0)
except:
    exit(1)
" 2>/dev/null; then
        echo "✅ PostgreSQL is ready!"
        break
    fi
    echo "   Attempt $i/30 - PostgreSQL not ready yet, waiting..."
    sleep 2
done

# Initialize database tables
echo "🗄️  Initializing database tables..."
python init_db.py || echo "⚠️  Database initialization warning (tables may already exist)"

# Start the application
echo "🚀 Starting NestWorth API server..."
exec "$@"
