from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить клиента", callback_data="add_client")],
            [InlineKeyboardButton(text="📋 Список клиентов", callback_data="list_clients")],
            [InlineKeyboardButton(text="✏ Установить статус", callback_data="set_status")],
            [InlineKeyboardButton(text="🗑 Удалить клиента", callback_data="delete_client")],
        ]
    )