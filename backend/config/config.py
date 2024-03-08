# config.py

import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
