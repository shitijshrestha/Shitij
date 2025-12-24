# IPTV Recorder Bot

A fully functional Telegram bot to record IPTV streams (M3U8 or direct links) and upload videos to Telegram.  
Supports VPS, Render, or Termux deployment.  

---

## ✅ Features

- Record streams with `/record` or `/rec` command.
- Record using `/p1` command (direct URL only, no playlist required).
- Admin-only access with `/addadmin <user_id>`.
- Uploads handled via `uploader.py`.
- Automatically deletes recordings after upload.
- Works on VPS, Termux, and Render without additional configuration.
- No `playlist.json` required — all commands work standalone.

---

## ⚙️ Requirements

- Python 3.11+  
- Pyrogram
- ffmpeg installed on the system
- `uploader.py`, `config.py` present

---

## 📂 Files

- `bot.py` — Main bot code (updated version)  
- `uploader.py` — Handles uploads to Telegram  
- `config.py` — Bot configuration (API_ID, API_HASH, BOT_TOKEN, PERMANENT_ADMIN, RECORDINGS_DIR, MAX_UPLOAD_SIZE)  
- `recorder.py`, `main.py` — Existing helper files  
- Deployment files: `Dockerfile`, `render.yaml`, `Procfile`  

---

## 🔧 Configuration

`config.py` contains:

```python
API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
PERMANENT_ADMIN = 123456789
RECORDINGS_DIR = "recordings"
MAX_UPLOAD_SIZE = 2000  # in MB
