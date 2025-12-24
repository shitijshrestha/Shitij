import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN, PERMANENT_ADMIN
from recorder import record_stream

client = TelegramClient("recordbot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
approved_users = {PERMANENT_ADMIN}

@client.on(events.NewMessage(pattern="/start"))
async def start_cmd(event):
    await event.reply("🤖 Welcome! Use /record <url> <duration> <title>")

@client.on(events.NewMessage(pattern=r"^/record "))
async def record_cmd(event):
    if event.sender_id not in approved_users:
        return await event.reply("🚫 Not authorized.")
    try:
        _, url, duration, title = event.text.split(" ",3)
        asyncio.create_task(record_stream(client, event.chat_id, url, duration, title))
    except ValueError:
        await event.reply("❌ Usage: /record <url> <duration> <title>")

@client.on(events.NewMessage(pattern=r"^/addadmin "))
async def addadmin_cmd(event):
    if event.sender_id != PERMANENT_ADMIN:
        return await event.reply("🚫 Only permanent admin can add users.")
    try:
        uid = int(event.text.split(" ",1)[1])
        approved_users.add(uid)
        await event.reply(f"✅ User {uid} added.")
    except:
        await event.reply("❌ Usage: /addadmin <user_id>")

print("🤖 Bot started successfully with 2GB split upload support.")
client.run_until_disconnected()