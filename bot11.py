from fastapi import FastAPI
from pyrogram import Client, filters
from pyrogram.types import Message
from contextlib import asynccontextmanager
import asyncio

API_ID = 20366208
API_HASH = "2c9d5b3859f56347838f388c59377bd9"
BOT_TOKEN = "7186450162:AAHfqp6rQlnNgpOon5qTCTA4CoRVd_ZBTV8"
VIDEO_CHANNEL = -1002544364347

bot = Client("raredesistuffbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Pyrogram bot
    await bot.start()
    print("✅ Bot started")
    yield
    await bot.stop()
    print("🛑 Bot stopped")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"status": "Bot is running"}

@bot.on_message(filters.private & filters.command("start"))
async def handle_start(client: Client, message: Message):
    args = message.command
    if len(args) > 1:
        param = args[1]
        if param.startswith("vid") and param[3:].isdigit():
            msg_id = int(param[3:])
            try:
                await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=VIDEO_CHANNEL,
                    message_id=msg_id
                )
            except Exception as e:
                await message.reply(f"❌ Could not fetch video: {e}")
        else:
            await message.reply("❗ Invalid video key.")
    else:
        await message.reply("👋 Send /start to get a video.")
