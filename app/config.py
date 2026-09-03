import os
from dotenv import load_dotenv

load_dotenv()

_raw_url = os.getenv("DATABASE_URL", "")
# psycopg3 requires postgresql+psycopg:// scheme
DATABASE_URL = _raw_url.replace("postgresql://", "postgresql+psycopg://", 1) if _raw_url.startswith("postgresql://") else _raw_url
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
