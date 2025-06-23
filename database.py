"""
Ma'lumotlar bazasi bilan ishlash moduli
"""
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import config

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Ma'lumotlar bazasi modellari uchun asosiy sinf"""
    pass


# Async engine yaratish
engine = create_async_engine(
    config.DATABASE_URL,
    echo=False,
    future=True
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Ma'lumotlar bazasi sessiyasini olish"""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Ma'lumotlar bazasi xatosi: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Ma'lumotlar bazasini yaratish"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Ma'lumotlar bazasi muvaffaqiyatli yaratildi")


async def close_db() -> None:
    """Ma'lumotlar bazasi ulanishini yopish"""
    await engine.dispose()
    logger.info("Ma'lumotlar bazasi ulanishi yopildi")