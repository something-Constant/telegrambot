from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message
from aiogram.exceptions import TelegramRetryAfter

# =========================
# CONFIG
# =========================

TOKEN = "7058704613:AAEuFunpv6m3jogUOXFR-0rEBrYmuQkxQh0"


WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://mohamadmeymandi.leapcell.app{WEBHOOK_PATH}"

HOST = "0.0.0.0"
PORT = 8080

# =========================
# BOT
# =========================

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()


# =========================
# HANDLERS
# =========================

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Bot is running 🚀")


dp.include_router(router)


# =========================
# FASTAPI LIFESPAN
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting bot...")

    try:
        webhook_info = await bot.get_webhook_info()

        # avoid flood control
        if webhook_info.url != WEBHOOK_URL:
            await bot.set_webhook(WEBHOOK_URL)
            print(f"Webhook set: {WEBHOOK_URL}")
        else:
            print("Webhook already set.")

    except TelegramRetryAfter as e:
        print(f"Retry after: {e.retry_after}")

    yield

    print("Shutting down bot...")
    await bot.delete_webhook(drop_pending_updates=False)
    await bot.session.close()


# =========================
# FASTAPI APP
# =========================

app = FastAPI(lifespan=lifespan)


# healthcheck for Leapcell
@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/kaithhealthcheck")
async def healthcheck():
    return {"status": "healthy"}


@app.get("/kaithheathcheck")
async def healthcheck_typo():
    return {"status": "healthy"}


# telegram webhook
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()

    update = Update.model_validate(data)

    await dp.feed_update(bot, update)

    return {"ok": True}


# =========================
# LOCAL RUN
# =========================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=False,
    )