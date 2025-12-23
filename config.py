import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # # To handle database connection stability
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     "pool_pre_ping": True,  # Checks connection health before every query
    #     "pool_recycle": 300,    # Re-opens connections every 5 minutes
    # }
    
    if not SECRET_KEY or not SQLALCHEMY_DATABASE_URI:
        raise ValueError("Missing required environment variables")

