import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update, BotCommand, BotCommandScopeDefault

# Local imports
from config import TOKEN
from Database.database import create_tables
from Handlers.Keyboards import keyboard_router
from Handlers.Global_Commands import globalcommand_router


# ========================= CONFIG =========================
BASE_URL = "https://mohamadmeymandi.leapcell.app"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"


bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

dp.include_router(globalcommand_router)
dp.include_router(keyboard_router)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Help"),
        BotCommand(command="menu", description="Main menu"),
        BotCommand(command="setting", description="Settings"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set: {WEBHOOK_URL}")

    await create_tables()
    await set_commands(bot)
    
    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": "error"}


@app.get("/")
async def index():
    return {"status": "Bot is running on Leapcell"}


# Local test
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)