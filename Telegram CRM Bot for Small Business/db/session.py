from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
