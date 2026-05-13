from aiogram import Router
from aiogram import types
from aiogram.filters import Command

### Local Module

from .Keyboards import menu_keyboard
from ..Database.database import add_user, search_user

globalcommand_router = Router()


@globalcommand_router.message(Command("start"))
async def start_handler(message: types.Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        name=message.from_user.full_name,
    )
    await message.delete()
    await message.answer("Welcome", reply_markup=menu_keyboard)


@globalcommand_router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.delete()

    await message.answer("help:")


@globalcommand_router.message(Command("setting"))
async def setting_handler(message: types.Message):
    await message.delete()

    await message.answer("setting:")


@globalcommand_router.message(Command("menu"))
async def menu_handler(message: types.Message):
    await message.delete()
    id = await message.answer("📃", reply_markup=menu_keyboard)

    # await id.delete()

    # await message.bot.delete_message(chat_id=message.chat.id, message_id=id.message_id)
