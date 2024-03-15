import os

from dotenv import load_dotenv


load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_URL_ALEMBIC = os.getenv("POSTGRES_URL_ALEMBIC")