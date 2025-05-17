from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_AI")
BASEROW_URL = os.getenv("BASEROW_URL")
BASEROW_TOKEN = os.getenv("BASEROW_TOKEN")
BASEROW_EMAIL = os.getenv("BASEROW_EMAIL")
BASEROW_PASSWORD = os.getenv("BASEROW_PASSWORD")
