import os

# -------- TELEGRAM CONFIG --------
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# -------- ADMIN CONFIG --------
PERMANENT_ADMIN = int(os.getenv("PERMANENT_ADMIN", "0"))
DUMP_CHANNEL_ID = int(os.getenv("DUMP_CHANNEL_ID", "0"))

# -------- RECORDING CONFIG --------
RECORDINGS_DIR = os.getenv("RECORDINGS_DIR", "./recordings")
MAX_TELEGRAM_SIZE = 2 * 1024 * 1024 * 1024  # 2GB