import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://api.football-data.org/v4"
API_TOKEN = os.getenv("API_TOKEN")

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
DEFAULT_EMAIL = "sjolly03@gmail.com"

DEFAULT_TIMEZONE = "America/New_York"