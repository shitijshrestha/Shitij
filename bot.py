import os
import json
import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from config import (
    API_ID, API_HASH, BOT_TOKEN, PERMANENT_ADMIN,
    RECORDINGS_DIR, MAX_UPLOAD_SIZE
)
from uploader import upload_video  # ✅ uploader.py se upload function

os.makedirs(RECORDINGS_DIR, exist_ok=True)

app = Client(
    "iptv_recorder_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

ADMINS = {PERMANENT_ADMIN}
USERS = set()
PLAYLIST_FILE = "playlist.json"

# ---------------- HELPERS ----------------
def is_admin(uid): return uid in ADMINS
def is_allowed(uid): return uid in ADMINS or uid in USERS

def load_playlist():
    if os.path.exists(PLAYLIST_FILE):
        with open(PLAYLIST_FILE, "r") as f:
            return json.load(f)
    return {}

def save_playlist(data):
    with open(PLAYLIST_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------------- COMMANDS ----------------
@app.on_message(filters.command("start"))
async def start_cmd(_, m: Message):
    if m.from_user.id not in USERS and not is_admin(m.from_user.id):
        USERS.add(m.from_user.id)
    await m.reply_text(
        "👋 IPTV Recorder Bot\n\n"
        "Commands:\n"
        "/record <url> <HH:MM:SS>\n"
        "/rec <url> <HH:MM:SS>\n"
        "/pl <name> <url>\n"
        "/p1 <name> <HH:MM:SS>\n"
        "/find <name>\n"
        "/addadmin <id>\n"
        "/help"
    )

@app.on_message(filters.command("help"))
async def help_cmd(_, m: Message):
    await m.reply_text(
        "**Help Menu**\n"
        "/record url 00:05:00\n"
        "/rec url 00:05:00\n"
        "/pl name url (add playlist)\n"
        "/p1 name 00:05:00 (record playlist)\n"
        "/find name\n"
        "/addadmin id"
    )

@app.on_message(filters.command("addadmin"))
async def add_admin(_, m: Message):
    if not is_admin(m.from_user.id):
        return await m.reply_text("❌ Admin only")
    if len(m.command) != 2:
        return await m.reply_text("Usage: /addadmin <user_id>")
    uid = int(m.command[1])
    ADMINS.add(uid)
    await m.reply_text(f"✅ Admin added: `{uid}`")

@app.on_message(filters.command("pl"))
async def add_playlist(_, m: Message):
    if not is_admin(m.from_user.id):
        return await m.reply_text("❌ Admin only")
    if len(m.command) < 3:
        return await m.reply_text("Usage: /pl <name> <url>")
    name = m.command[1].lower()
    url = m.command[2]
    data = load_playlist()
    data[name] = url
    save_playlist(data)
    await m.reply_text(f"✅ Playlist added: `{name}`")

@app.on_message(filters.command("find"))
async def find_playlist(_, m: Message):
    data = load_playlist()
    if len(m.command) != 2:
        return await m.reply_text("Usage: /find <name>")
    key = m.command[1].lower()
    matches = [k for k in data if key in k]
    if not matches:
        return await m.reply_text("❌ No match found")
    text = "**Found Channels:**\n" + "\n".join(f"- `{k}`" for k in matches)
    await m.reply_text(text)

# ---------------- RECORD FUNCTION ----------------
async def do_record(m, url, duration):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = f"{RECORDINGS_DIR}/rec_{now}.mp4"
    status_msg = await m.reply_text("🎬 Recording started...")
    
    cmd = ["ffmpeg", "-y", "-i", url, "-t", duration, "-c", "copy", outfile]
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
    )
    await proc.communicate()
    
    if not os.path.exists(outfile):
        return await status_msg.edit("❌ Recording failed")
    
    size_mb = os.path.getsize(outfile) / (1024*1024)
    if size_mb > MAX_UPLOAD_SIZE:
        os.remove(outfile)
        return await status_msg.edit("❌ File too large")
    
    await status_msg.edit("📤 Uploading to Telegram...")
    
    # ---------------- USE uploader.py ----------------
    await upload_video(app, m.chat.id, outfile, caption=f"🎥 Recorded\n⏱ {duration}")
    
    os.remove(outfile)
    await status_msg.delete()

# ---------------- RECORD COMMANDS ----------------
@app.on_message(filters.command(["record","rec"]))
async def record_cmd(_, m: Message):
    if not is_allowed(m.from_user.id):
        return await m.reply_text("❌ Not allowed")
    if len(m.command) < 3:
        return await m.reply_text("Usage: /record <url> <HH:MM:SS>")
    await do_record(m, m.command[1], m.command[2])

@app.on_message(filters.command("p1"))
async def playlist_record(_, m: Message):
    if not is_allowed(m.from_user.id):
        return await m.reply_text("❌ Not allowed")
    if len(m.command) < 3:
        return await m.reply_text("Usage: /p1 <name> <HH:MM:SS>")
    name = m.command[1].lower()
    duration = m.command[2]
    data = load_playlist()
    if name not in data:
        return await m.reply_text("❌ Playlist not found")
    await do_record(m, data[name], duration)

# ---------------- RUN ----------------
if __name__ == "__main__":
    print("✅ IPTV Recorder Bot running...")
    app.run()
