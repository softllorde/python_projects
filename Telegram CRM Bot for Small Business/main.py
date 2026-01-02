import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from config import TOKEN
from bot.handlers.start_handler import start_router
from bot.handlers.admin_handler import admin_router
from db.base import Base
from db.session import engine

bot = Bot(token=TOKEN)

dp = Dispatcher()
dp.include_routers(start_router, admin_router)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
	await init_db()
	await dp.start_polling(bot)

asyncio.run(main())