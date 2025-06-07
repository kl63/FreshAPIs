#!/usr/bin/env python3
from sqlalchemy import create_engine, text
import os
import sys

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to sys.path
sys.path.insert(0, current_dir)

# Import database configuration
from database.database import engine

def list_tables():
    """List all tables in the database."""
    with engine.connect() as conn:
        # PostgreSQL query to list all tables in the current schema
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = result.fetchall()
        
        print("Tables in database:")
        for table in tables:
            print(f"- {table[0]}")

if __name__ == "__main__":
    list_tables()
