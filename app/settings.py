import os

from dotenv import load_dotenv

load_dotenv("local.env")

DATABASE_URL: str = os.getenv("DATABASE_URL")
OVERRIDE_DATABASE_URL: str = os.getenv("OVERRIDE_DATABASE_URL")
