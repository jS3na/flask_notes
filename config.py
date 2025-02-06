import os
from dotenv import load_dotenv
import psycopg2
import redis

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class ApplicationConfig:

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(os.getenv("REDIS_URL"))
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
