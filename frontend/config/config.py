# config.py

import os
from dotenv import load_dotenv
load_dotenv()

FASTAPI_ENV = os.getenv("FASTAPI_ENV", "development")

