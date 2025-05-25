"""Database configuration and models for BriefNews API"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create SQLAlchemy base class
Base = declarative_base()

class Article(Base):
    """Article model for storing news articles"""
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    url = Column(String(500), unique=True, nullable=False)
    summary = Column(Text)
    authors = Column(String(500), nullable=False)
    published_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Article(title='{self.title}', url='{self.url}')>"

# Database connection setup
def get_db_connection():
    """Create database connection"""
    # For development, use SQLite. For production, use PostgreSQL
    DATABASE_URL = "sqlite:///./briefnews.db"  # Change this to your PostgreSQL URL in production
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def init_db():
    """Initialize database and create tables"""
    DATABASE_URL = "sqlite:///./briefnews.db"  # Change this to your PostgreSQL URL in production
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine) 