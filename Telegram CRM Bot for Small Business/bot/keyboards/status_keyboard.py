from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.statuses import ClientStatus


def status_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ClientStatus.NEW.value,
                    callback_data=f"status:{ClientStatus.NEW.name}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=ClientStatus.IN_PROGRESS.value,
                    callback_data=f"status:{ClientStatus.IN_PROGRESS.name}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=ClientStatus.DONE.value,
                    callback_data=f"status:{ClientStatus.DONE.name}"
                )
            ],
        ]
    )
