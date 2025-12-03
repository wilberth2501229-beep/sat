"""Create database tables directly"""
from app.core.database import engine, Base
from app.models import *  # Import all models

if __name__ == "__main__":
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
