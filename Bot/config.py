from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "7058704613:AAEuFunpv6m3jogUOXFR-0rEBrYmuQkxQh0"

def generate_keyboard(
    size: int = 2, keys: dict = {}, keybuilder: isinstance = InlineKeyboardBuilder()
) -> any:
    for item in keys:
        keybuilder.button(text=item, callback_data=f"{keys[item]}")

    keybuilder.adjust(size)

    return keybuilder.as_markup(resize_keyboard=True)
    