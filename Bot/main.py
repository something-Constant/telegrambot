import asyncio
import logging
import os

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


# Run the bot
async def main() -> None:
    try:
        session = AiohttpSession(proxy="http://127.0.0.1:23010")
        await create_tables()

        bot = Bot(token=TOKEN, session=session)
        logging.basicConfig(level=logging.INFO)
        await set_commands(bot)


        
        print("Bot is running...")
        await Root.start_polling(bot)

    except Exception as e:
        if e is KeyboardInterrupt:
            os.system("cls")
            quit()

        else:
            print(e)


if __name__ == "__main__":
    asyncio.run(main())
