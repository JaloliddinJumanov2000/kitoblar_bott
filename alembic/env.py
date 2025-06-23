"""
Alembic muhit konfiguratsiyasi
"""
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from config import config as app_config
from database import Base

# Alembic Config obyekti
config = context.config

# Logging konfiguratsiyasi
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ma'lumotlar bazasi URL ni o'rnatish
config.set_main_option("sqlalchemy.url", app_config.DATABASE_URL)

# Metadata obyekti
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Offline migratsiyalar"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Migratsiyalarni amalga oshirish"""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Async migratsiyalar"""
    connectable = create_async_engine(
        app_config.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Online migratsiyalar"""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()