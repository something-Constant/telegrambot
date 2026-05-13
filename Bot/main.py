import os
from aiogram import Bot, Dispatcher
from aiogram.types import Update

from aiogram import Router


from aiogram import F, loggers, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
)


from contextlib import asynccontextmanager
import sys

from fastapi import FastAPI, Request
from aiogram.exceptions import TelegramRetryAfter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

### Local Module
# from Bot.config import TOKEN, generate_keyboard
# from Bot.Handlers.Keyboards import keyboard_router
from Bot.Handlers.Global_Commands import globalcommand_router

# from DataBase.database import globalcommand_router
from Bot.Database.database import create_tables

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = "02i39u8hg82ybo"

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://mohamadmeymandi.leapcell.app{WEBHOOK_PATH}"
HOST = "0.0.0.0"
PORT = 8080


bot = Bot(token=TOKEN)

### routing
Root = Dispatcher()
router = Router()
Root.include_router(router)
Root.include_router(globalcommand_router)
# Root.include_router(keyboard_router)


### makeing the inline base menus
inline_builder = InlineKeyboardBuilder()
inline_keys = {"⬅ Back": "Back", "▶ Start": "Start", "❌ Cancel": "Cancel"}

for item in inline_keys:
    inline_builder.button(text=item, callback_data=f"{inline_keys[item]}")
inline_builder.adjust(2, 1)
inline_keyboard = inline_builder.as_markup(resize_keyboard=True)

# @router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
# async def on_user_leave(event: types.ChatMemberUpdated):
#     pass


# @router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
# async def on_user_join(event: types.ChatMemberUpdated):
#     pass


@router.error()
async def error_handler(event: types.ErrorEvent):
    loggers.critical("Critical error caused by %s", event.exception, exc_info=True)


@router.callback_query(F.data == "cancel")
async def back(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Start the bot / Restart"),
        types.BotCommand(command="help", description="Help & instructions"),
        types.BotCommand(command="menu", description="Show main menu"),
        types.BotCommand(command="setting", description="Bot settings ⚙️"),
    ]

    await bot.set_chat_menu_button(menu_button=types.MenuButtonCommands(text="Menu"))

    success = await bot.set_my_commands(
        commands=commands,
        scope=types.BotCommandScopeDefault(),  # default = for all private chats
        # language_code="ru"             # optional: for specific language
    )

    return success  # True on success


# =========================
# FASTAPI LIFESPAN
# =========================


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting bot...")

    try:
        await create_tables()
        await set_commands(bot)

        webhook_info = await bot.get_webhook_info()

        # avoid flood control
        if webhook_info.url != WEBHOOK_URL:
            await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
            print(f"Webhook set: {WEBHOOK_URL}")
        else:
            print("Webhook already set.")

    except TelegramRetryAfter as e:
        print(f"Retry after: {e.retry_after}")

    yield

    print("Shutting down bot...")
    await bot.delete_webhook(drop_pending_updates=True)
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

    await Root.feed_update(bot, update)

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
