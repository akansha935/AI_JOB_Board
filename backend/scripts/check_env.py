from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

gemini_key = os.getenv("GEMINI_API_KEY")
database_url = os.getenv("DATABASE_URL")

print("Environment file:", env_path)
print("Gemini key loaded:", bool(gemini_key and "your_" not in gemini_key))
print("Database URL loaded:", bool(database_url and "your_" not in database_url))

if database_url:
    print("Database host present:", "@" in database_url)