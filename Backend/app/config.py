from dotenv import load_dotenv
import os

#Load data from .env
load_dotenv()  

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    # MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL= 'redis://localhost:6379/'