from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание асинхронной сессии
async_session_maker = sessionmaker(engine, class_=AsyncSession, autoflush=False, autocommit=False)

# Это не обязательная часть, но если хотите использовать `Base` для моделей, можете оставить:
Base = declarative_base()

# Асинхронная функция для инициализации базы данных
# Создание таблиц
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
