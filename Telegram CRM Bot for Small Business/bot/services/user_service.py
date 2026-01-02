from sqlalchemy import select
from db.models import User
from db.session import AsyncSessionLocal
from config import ADMINS


class UserService:

    async def get_or_create_user(self, telegram_id: int, username: str | None):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalars().first()

            if user:
                return user

            role = "admin" if telegram_id in ADMINS else "user"

            user = User(
                telegram_id=telegram_id,
                username=username,
                role=role
            )

            session.add(user)
            await session.flush()
            await session.commit()

            return user

    async def is_admin(self, telegram_id: int) -> bool:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalars().first()
            return bool(user and user.role == "admin")
