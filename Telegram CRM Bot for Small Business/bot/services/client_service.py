from sqlalchemy import select
from db.models import Client
from db.session import AsyncSessionLocal
from bot.utils.phone import normalize_phone


class ClientService:

    async def create_client(self, name: str, phone: str):
        phone = normalize_phone(phone)

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Client).where(Client.phone == phone)
            )
            existing = result.scalars().first()

            if existing:
                raise ValueError("Клиент с таким номером уже существует")

            client = Client(
                name=name,
                phone=phone
            )

            session.add(client)
            await session.flush()   # ОБЯЗАТЕЛЬНО
            await session.commit()

            return client

    async def get_client_by_phone(self, phone: str) -> Client | None:
        phone = normalize_phone(phone)

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Client).where(Client.phone == phone)
            )
            return result.scalars().first()

    async def update_status(self, phone: str, status: str):
        phone = normalize_phone(phone)

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Client).where(Client.phone == phone)
            )
            client = result.scalars().first()

            if not client:
                raise ValueError("Клиент не найден")

            client.status = status
            await session.commit()

            return client

    async def delete_client(self, phone: str):
        phone = normalize_phone(phone)

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Client).where(Client.phone == phone)
            )
            client = result.scalars().first()

            if not client:
                raise ValueError("Клиент не найден")

            await session.delete(client)
            await session.commit()

    async def get_all_clients(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Client))
            return result.scalars().all()
