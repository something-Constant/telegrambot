from aiogram import Router
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F, Bot
from aiogram.types import ChatMember
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

##########3
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonRequestChat,
)


keyboard_router = Router()

### makeing the reply base menus
keyboard_item = ["🧾 Report", "📌 Help", "📊 Status", "⚙️ Settings"]
keyboard_builder = ReplyKeyboardBuilder()
menu_keyboard = []

for item in keyboard_item:
    keyboard_builder.button(text=item)

keyboard_builder.adjust(1, 3)

menu_keyboard = keyboard_builder.as_markup(resize_keyboard=True)


# Command handler
@keyboard_router.message(F.text == keyboard_item[0])
async def report_handler(message: types.Message) -> None:
    await message.delete()

    await message.answer("report")


@keyboard_router.message(F.text == keyboard_item[1])
async def help_handler(message: types.Message) -> None:
    await message.delete()

    await message.answer("help")


@keyboard_router.message(F.text == keyboard_item[2])
async def status_handler(message: types.Message, bot) -> None:
    await message.delete()

    member: ChatMember = await message.bot.get_chat_member(
        "-1001638822794", message.from_user.id
    )

    print(member)
    print(member.status)

    await message.answer("status")


@keyboard_router.message(F.text == keyboard_item[3])
async def settings_handler(message: types.Message) -> None:
    await message.delete()
    try:
        member = await message.bot.get_chat("@DrTel18")
        print(member.id)
        await message.answer(str(member.id))
        print(message.html_text)

    except Exception as e:
        # Handle cases: chat not found, user not found, etc.
        print(f"Error checking membership: {e}")

    await message.answer("setting")


@keyboard_router.message(F.text.startswith("id:"))
async def ids_handler(message: types.Message) -> None:

    await message.reply("Sen dlike this → id: @foo")

    try:
        user_text: str
        user_text = message.html_text.strip()
        user_text = user_text[user_text.find("@") :]

        chat = await message.bot.get_chat(user_text)
        await message.reply(str(chat.id))
        print(message.html_text)

    except Exception as e:
        # Handle cases: chat not found, user not foundq, etc.
        print(f"Error checking membership: {e}")
        await message.reply(str(e))


# @keyboard_router.message()
# async def any_message_handler(message: types.Message):
#     chat_id = message.chat.id  # This is the chat ID you need[citation:3]
#     await message.answer(f"This chat's ID is: {chat_id}")


async def is_user_member(bot: Bot, chat_id: int | str, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)

        if member.status in ["member", "administrator", "creator"]:
            return True

    except Exception:
        return False


@keyboard_router.message(F.text == "select")
async def select_chat(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📢 Select a channel / group",
                    request_chat=KeyboardButtonRequestChat(
                        request_id=1,
                        chat_is_channel=True,  # None = group OR channel
                        chat_is_forum=False,
                        chat_has_username=False,
                        chat_is_created=False,

                    ),
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer("Please select a chat:", reply_markup=keyboard)


@keyboard_router.message()
async def chat_shared(message: Message):
    if message.chat_shared:
        chat_id = message.chat_shared.chat_id
        request_id = message.chat_shared.request_id

        await message.answer(
            f"✅ Chat received!\n"
            f"Chat ID: {chat_id}\n"
            f"Request ID: {request_id}"
        )