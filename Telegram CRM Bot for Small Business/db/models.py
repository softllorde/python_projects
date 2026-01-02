from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    role = Column(String, default="user")  # "admin" / "user"
    created_at = Column(DateTime, default=datetime.utcnow)

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    status = Column(String, default="new")  # new / in_progress / completed / canceled
    created_at = Column(DateTime, default=datetime.utcnow)