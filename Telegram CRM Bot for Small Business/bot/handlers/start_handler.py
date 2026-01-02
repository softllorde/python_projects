from aiogram import types, Router
from aiogram.filters import CommandStart
from bot.services.user_service import UserService

user_service = UserService()

start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(message: types.Message):
	await user_service.get_or_create_user(telegram_id=message.from_user.id, username=message.from_user.username)
	await message.answer("Зарегестрирован!")