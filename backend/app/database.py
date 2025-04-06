"""
Database connection and session management for the application.
This module sets up SQLAlchemy with PostgreSQL and provides session management utilities.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection settings from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "production-db-host")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ai_recommendation")

# Construct database URL
DB_DRIVER = os.getenv("DB_DRIVER", "postgresql")
DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "False").lower() == "true",  # SQL echo for debugging
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),  # Connection pool size
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),  # Max overflow connections
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a thread-local session
db_session = scoped_session(SessionLocal)

# Create declarative base class for models
Base = declarative_base()
Base.query = db_session.query_property()

def get_db():
    """
    Get a database session.
    
    Returns:
        SQLAlchemy session: A database session
        
    Usage:
        with get_db() as db:
            db.query(Model).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables.
    
    This should be called when the application starts.
    """
    # Import all models here to ensure they are registered with the Base
    from app.models import User, Course, UserCourseInteraction, Recommendation
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
