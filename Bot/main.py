import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response

from aiogram import Bot, Dispatcher, Router, F, loggers, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Update
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Local modules
from Bot.config import TOKEN
# from Handlers.Keyboards import keyboard_router
# from Handlers.Global_Commands import globalcommand_router
# from Database.database import create_tables


logging.basicConfig(level=logging.INFO)

BASE_URL = "https://mohamadmeymandi.leapcell.app"
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"


# Bot
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

# Dispatcher
dp = Dispatcher()
router = Router()

# dp.include_router(router)
# dp.include_router(globalcommand_router)
# dp.include_router(keyboard_router)


# FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting bot...")

    # await create_tables()

    # Remove old webhook updates
    await bot.delete_webhook(
        drop_pending_updates=True
    )

    # Set new webhook
    await bot.set_webhook(WEBHOOK_URL)

    print(f"Webhook set: {WEBHOOK_URL}")

    yield

    print("Stopping bot...")

    await bot.delete_webhook()

    await bot.session.close()

    print("Bot stopped")


# FastAPI app
app = FastAPI(lifespan=lifespan)


# Inline keyboard
inline_builder = InlineKeyboardBuilder()

inline_keys = {
    "⬅ Back": "Back",
    "▶ Start": "Start",
    "❌ Cancel": "Cancel",
}

for text, callback in inline_keys.items():
    inline_builder.button(
        text=text,
        callback_data=callback
    )

inline_builder.adjust(2, 1)

inline_keyboard = inline_builder.as_markup()


# Global error handler
@router.error()
async def error_handler(event: types.ErrorEvent):

    loggers.event.exception(
        "Critical error caused by %s",
        event.exception
    )


# Cancel button
@router.callback_query(F.data == "Cancel")
async def cancel_handler(
    call: types.CallbackQuery,
    state: FSMContext
):

    await state.clear()

    await call.message.delete()

    await call.answer()


# Telegram webhook
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):

    try:
        update_data = await request.json()

        update = Update.model_validate(
            update_data,
            context={"bot": bot}
        )

        await dp.feed_update(bot, update)

    except Exception as e:

        logging.exception(e)

        return Response(
            status_code=500,
            content="error"
        )

    return Response(
        status_code=200,
        content="ok"
    )