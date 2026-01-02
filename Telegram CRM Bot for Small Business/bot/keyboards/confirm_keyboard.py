from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_delete_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да, удалить", callback_data="confirm_delete_yes"),
                InlineKeyboardButton(text="❌ Отмена", callback_data="confirm_delete_no"),
            ]
        ]
    )