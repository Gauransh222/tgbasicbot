from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os

API_ID = 20366208
API_HASH = "2c9d5b3859f56347838f388c59377bd9"
BOT_TOKEN = "7186450162:AAHfqp6rQlnNgpOon5qTCTA4CoRVd_ZBTV8"

CHANNEL_1 = -1002544364347  # Your video storage private channel

# Store video file_id mapped by key like "vid15"
video_store = {}

# Pyrogram client (bot)
bot = Client("tgbasicbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# FastAPI app for Render & uptime
app = FastAPI()

# ✅ Support both GET and HEAD requests for uptime check
@app.api_route("/", methods=["GET", "HEAD"])
def root(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content=None, status_code=200)
    return {"status": "Bot is running"}

# 📦 Store file_id when bot receives a video
@bot.on_message(filters.chat(CHANNEL_1) & filters.video)
async def handle_video(client, message: Message):
    key = f"vid{message.id}"
    video_store[key] = message.video.file_id
    print(f"Saved: {key} → {message.video.file_id}")

# 🚀 Respond to deep links like /start vid15
@bot.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    parts = message.text.split(" ")
    if len(parts) == 2 and parts[1].startswith("vid"):
        key = parts[1]
        file_id = video_store.get(key)
        if file_id:
            await message.reply_video(file_id, caption="🎬 Here's your video")
        else:
            await message.reply("❌ Video not found. It may have expired or the bot was restarted.")
    else:
        await message.reply("👋 Welcome! Use a valid video link.")

# 🔄 Launch bot and API together
@app.on_event("startup")
async def startup():
    await bot.start()
    print("✅ Bot started")

@app.on_event("shutdown")
async def shutdown():
    await bot.stop()
    print("❌ Bot stopped")
