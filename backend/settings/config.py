import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path('.') / '.env')

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
DATABASE_URL = os.getenv("DATABASE_URL", "localhost")
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
