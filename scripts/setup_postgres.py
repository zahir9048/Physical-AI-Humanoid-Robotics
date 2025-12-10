#!/usr/bin/env python3
"""
Setup script for Neon Postgres database
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Add the backend/src directory to the path so we can import our modules
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_src_dir = os.path.join(script_dir, '..', 'backend', 'src')
sys.path.insert(0, backend_src_dir)

from core.config import settings
from models.conversation import Conversation
from models.message import Message as MessageModel
from models.feedback import Feedback

def setup_postgres():
    print("Setting up Postgres database...")

    try:
        # Create database engine
        engine = create_engine(settings.DATABASE_URL)

        # Test the connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database connection successful")

        # Create tables
        from core.database import Base
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")

        # Verify tables were created
        with engine.connect() as connection:
            # Check if our tables exist
            result = connection.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name IN ('conversations', 'messages', 'feedback')
            """))

            created_tables = [row[0] for row in result.fetchall()]
            print(f"Created tables: {created_tables}")

    except OperationalError as e:
        print(f"Database connection error: {str(e)}")
        print("Make sure your DATABASE_URL is correctly configured in the environment variables.")
        return False
    except Exception as e:
        print(f"Error setting up Postgres: {str(e)}")
        return False

    print("Postgres setup completed successfully!")
    return True

if __name__ == "__main__":
    setup_postgres()