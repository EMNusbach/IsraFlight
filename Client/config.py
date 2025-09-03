import os
from dotenv import load_dotenv

load_dotenv()

# Get API base URL, fallback to localhost if not defined
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5126/api")
