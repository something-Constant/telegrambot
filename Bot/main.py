import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from aiogram import Bot, Dispatcher
from aiogram.types import Update, BotCommand, BotCommandScopeDefault
from aiogram.filters import Command

# Local imports
from config import TOKEN
from Database.database import create_tables

from Handlers.Keyboards import keyboard_router
from Handlers.Global_Commands import globalcommand_router


# ========================= CONFIG =========================
BASE_URL = "https://mohamadmeymandi.leapcell.app"   # ←←← CHANGE TO YOUR LEAPCELL URL
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"


# ========================= BOT & DISPATCHER =========================
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Include your routers
dp.include_router(globalcommand_router)
dp.include_router(keyboard_router)


# ======================== COMMANDS ========================
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot / Restart"),
        BotCommand(command="help", description="Help & instructions"),
        BotCommand(command="menu", description="Show main menu"),
        BotCommand(command="setting", description="Bot settings ⚙️"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault()
    )


# ======================== LIFESPAN ========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"✅ Webhook set successfully: {WEBHOOK_URL}")

    await create_tables()
    await set_commands(bot)
    
    yield

    # Shutdown
    await bot.delete_webhook()
    logging.info("Webhook deleted")


# ======================== FASTAPI APP ========================
app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return {"status": "error"}


@app.get("/")
async def index():
    return {"message": "✅ Telegram Bot is running on Leapcell!"}


# ======================== RUN (for local testing) ========================
if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)