from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from app.config_reader import PostgresConfig
from app.types.sqlalchemy import AsyncSessionMaker


def create_engine(config: PostgresConfig) -> AsyncEngine:
    return create_async_engine(
        config.dsn,
        echo=config.echo,
    )


def create_session_maker(engine: AsyncEngine) -> AsyncSessionMaker:
    return async_sessionmaker(engine, expire_on_commit=False)
