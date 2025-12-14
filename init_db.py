#!/usr/bin/env python3
"""
Database initialization script for NestWorth.

This script creates the database tables if they don't exist.
Run this before starting the API server.
"""
import sys
from packages.domain import db


def main():
    """Initialize the database tables."""
    print("🏗️  Initializing NestWorth database...")

    try:
        db.init_db()
        print("✅ Database initialized successfully!")
        print(f"   Connection: {db.get_database_url()}")
        return 0

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your DATABASE_URL in .env file")
        print("3. Ensure the database 'nestworth' exists")
        print("4. Verify database credentials")
        return 1


if __name__ == "__main__":
    sys.exit(main())
