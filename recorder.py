import os
import subprocess
import datetime
import asyncio
from config import RECORDINGS_DIR, MAX_TELEGRAM_SIZE
from uploader import upload_file

def time_to_seconds(t):
    if ":" in t:
        parts = list(map(int, t.split(":")))
        while len(parts) < 3:
            parts.insert(0,0)
        h,m,s = parts
        return h*3600 + m*60 + s
    return int(t)

async def record_stream(client, chat_id, url, duration_str, title):
    duration = time_to_seconds(duration_str)
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=duration)
    date_str = start.strftime("%d-%m-%Y")
    filename = f"{title}.{start.strftime('%H-%M-%S')}-{end.strftime('%H-%M-%S')}.{date_str}.mp4"
    filepath = os.path.join(RECORDINGS_DIR, filename)

    msg = await client.send_message(chat_id,
        f"🎬 <b>Recording Started</b>\n🎥 {title}\n⏱ Duration: {duration_str}\n🔗 URL: {url}",
        parse_mode="html"
    )

    cmd = [
        "ffmpeg","-y","-i",url,
        "-t",str(duration),
        "-c:v","libx264","-preset","veryfast",
        "-c:a","aac","-b:a","128k",
        filepath
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    start_ts = datetime.datetime.now().timestamp()

    while process.poll() is None:
        elapsed = int(datetime.datetime.now().timestamp() - start_ts)
        percent = min(100,(elapsed/duration)*100)
        bar = "█"*int(percent//10)+"░"*(10-int(percent//10))
        try:
            await msg.edit(f"🎥 <b>{title}</b>\n📊 {percent:.1f}% [{bar}]\n⏱ {elapsed}s / {duration}s",
                           parse_mode="html")
        except:
            pass
        await asyncio.sleep(5)

    process.wait()
    await client.send_message(chat_id,f"✅ Recording Finished.\n📤 Uploading <b>{title}</b>...",parse_mode="html")
    await upload_file(client, chat_id, filepath, title)
    await client.send_message(chat_id,f"✅ Upload completed for <b>{title}</b>",parse_mode="html")