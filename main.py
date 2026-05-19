from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import yt_dlp
import os
import asyncio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "MusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("بوت الميوزك يعمل بنجاح 🎵")

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("اكتب اسم الأغنية بعد الأمر")

    query = " ".join(message.command[1:])

    msg = await message.reply("جاري البحث...")

    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        url = info["url"]
        title = info["title"]

    await call_py.join_group_call(
        message.chat.id,
        MediaStream(url, audio_parameters=MediaStream.audio.high)
    )

    await msg.edit(f"تم تشغيل: {title}")

@app.on_message(filters.command("stop"))
async def stop(_, message):
    await call_py.leave_group_call(message.chat.id)
    await message.reply("تم إيقاف التشغيل")

async def main():
    await app.start()
    await call_py.start()
    print("Music Bot Started")
    await idle()

asyncio.run(main())
