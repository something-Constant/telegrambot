import asyncio
import logging
import os


from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.filters import Command

import flask, json
from flask import request, Flask
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


from aiogram.client.session.aiohttp import AiohttpSession

from aiogram import Bot, Dispatcher, F, Router, loggers, types
from aiogram.filters import (
    IS_MEMBER,
    IS_NOT_MEMBER,
    ChatMemberUpdatedFilter,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder,
    KeyboardBuilder,
)

from aiogram.methods import send_message

from aiogram.filters import Command

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from aiogram.fsm.state import StatesGroup, State

### Local Module
from config import TOKEN, generate_keyboard

from Handlers.Keyboards import keyboard_router
from Handlers.Global_Commands import globalcommand_router

# from DataBase.database import globalcommand_router

from Database.database import create_tables


# import Handlers.admin

app = Flask(__name__)


### routing
Root = Dispatcher()
router = Router()
Root.include_router(router)
Root.include_router(globalcommand_router)
Root.include_router(keyboard_router)


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


BASE_URL = "https://your-project-name.leapcell.app"   # ←←← CHANGE THIS
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"


bot = Bot(token=TOKEN, parse_mode="HTML")

# ======================== LIFESPAN ========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)
    
    yield
    
    # Shutdown
    await bot.delete_webhook()

# ======================== FASTAPI APP ========================
app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
        await Root.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error"}


@app.get("/")
async def index():
    return {"message": "Aiogram bot is running on Leapcell with FastAPI!"}
    
# Run the bot
async def main() -> None:
    try:
        # session = AiohttpSession(proxy="http://127.0.0.1:23010")
        # await create_tables()

        # bot = Bot(token=TOKEN, session=session, parse_mode="HTML")
        # logging.basicConfig(level=logging.INFO)
        # await set_commands(bot)

        # print("Bot is running...")
        # await Root.start_polling(bot)

        await create_tables()
        
        await set_commands(bot)



    except Exception as e:
        if e is KeyboardInterrupt:
            os.system("cls")
            quit()

        else:
            print(e)


if __name__ == "__main__":
    asyncio.run(main())
