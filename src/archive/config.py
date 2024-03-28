import os

from dotenv import load_dotenv


load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_URL_ALEMBIC = os.getenv("POSTGRES_URL_ALEMBIC")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE = os.getenv("ACCESS_TOKEN_EXPIRE")
REFRESH_TOKEN_EXPIRE = os.getenv("REFRESH_TOKEN_EXPIRE")