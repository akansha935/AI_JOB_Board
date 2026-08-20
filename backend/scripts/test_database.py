import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text

backend_dir = Path(__file__).resolve().parents[1]
env_path = backend_dir / ".env"

load_dotenv(env_path)

sys.path.insert(0, str(backend_dir))

from app.database import engine


with engine.connect() as connection:
    result = connection.execute(text("SELECT version()"))
    print("Database connection successful")
    print(result.scalar())