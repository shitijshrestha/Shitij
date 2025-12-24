import os
import asyncio
from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import FloodWaitError
from config import DUMP_CHANNEL_ID, MAX_TELEGRAM_SIZE

async def upload_file(client, chat_id, filepath, title):
    size = os.path.getsize(filepath)
    if size <= MAX_TELEGRAM_SIZE:
        await _upload(client, chat_id, filepath, title)
    else:
        # Split file
        parts = []
        with open(filepath, "rb") as f:
            index = 1
            while True:
                chunk = f.read(MAX_TELEGRAM_SIZE)
                if not chunk:
                    break
                part_path = f"{filepath}.part{index:03d}.mp4"
                with open(part_path, "wb") as pf:
                    pf.write(chunk)
                parts.append(part_path)
                index += 1
        # Upload each part
        for part in parts:
            await _upload(client, chat_id, part, title)
            os.remove(part)
        os.remove(filepath)

async def _upload(client, chat_id, filepath, title):
    import subprocess
    try:
        try:
            duration_output = subprocess.check_output([
                "ffprobe","-v","error","-show_entries",
                "format=duration","-of",
                "default=noprint_wrappers=1:nokey=1", filepath
            ]).decode().strip()
            duration = float(duration_output)
        except:
            duration = 0.0
        readable_size = f"{os.path.getsize(filepath)/1024/1024:.2f} MB"
        caption = (
            f"📁 <b>Filename:</b> {os.path.basename(filepath)}\n"
            f"⏱ <b>Duration:</b> {int(duration//3600):02d}:{int(duration%3600//60):02d}:{int(duration%60):02d}\n"
            f"📦 <b>Size:</b> {readable_size}\n"
            f"👨‍💻 Developer: @Shitijbro"
        )
        attributes = [
            DocumentAttributeVideo(duration=int(duration), w=1280, h=720, supports_streaming=True)
        ]
        # Upload to user
        await client.send_file(chat_id, filepath, caption=caption, parse_mode="html",
                               attributes=attributes, mime_type="video/mp4", supports_streaming=True)
        # Upload to dump
        await client.send_file(DUMP_CHANNEL_ID, filepath, caption=caption, parse_mode="html",
                               attributes=attributes, mime_type="video/mp4", supports_streaming=True)
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
        await _upload(client, chat_id, filepath, title)
    except Exception as e:
        await client.send_message(chat_id, f"⚠️ Upload failed: {e}")
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)