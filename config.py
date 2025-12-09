import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    if not SECRET_KEY or not SQLALCHEMY_DATABASE_URI:
        raise ValueError("Missing required environment variables")
