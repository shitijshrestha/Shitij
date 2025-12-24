import os
from dotenv import load_dotenv

load_dotenv()

# -------- TELEGRAM CONFIG --------
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# -------- ADMIN CONFIG --------
PERMANENT_ADMIN = int(os.getenv("PERMANENT_ADMIN", "0"))
DUMP_CHANNEL_ID = int(os.getenv("DUMP_CHANNEL_ID", "0"))

# -------- RECORDING CONFIG --------
RECORDINGS_DIR = os.getenv("RECORDINGS_DIR", "recordings")
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", "2000"))  # MB

# -------- MISC --------
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
