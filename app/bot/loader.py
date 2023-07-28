from datetime import timedelta

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import (
    DefaultKeyBuilder,
    RedisEventIsolation,
    RedisStorage,
)

from app.bot.handlers import setup_routers
from app.bot.middlewares import (
    ButtonsMiddleware,
    DBSessionMiddleware,
    I18nMiddleware,
    SyncUserMiddleware,
)
from app.bot.redis_custom_key_builder import UserIdKeyBuilder
from app.config_reader import Config
from app.services.db import create_engine, create_session_maker
from app.services.fluent import generate_hub
from app.services.redman import Redman


def create_bot(config: Config) -> Bot:
    return Bot(
        token=config.bot.token.get_secret_value(),
        parse_mode=ParseMode.HTML,
    )


async def on_startup(dispatcher: Dispatcher) -> None:
    config: Config = dispatcher["config"]
    redman: Redman = dispatcher["redman"]

    engine = create_engine(config.postgres)
    session_maker = create_session_maker(engine)
    dispatcher["session_maker"] = session_maker
    dispatcher.update.outer_middleware.register(
        DBSessionMiddleware(session_maker)
    )
    dispatcher.update.middleware.register(SyncUserMiddleware())
    translator_hub = generate_hub(config.fluent)
    dispatcher.workflow_data.update(translator_hub=translator_hub)
    dispatcher.update.outer_middleware.register(I18nMiddleware(translator_hub))

    dispatcher.update.middleware.register(ButtonsMiddleware())

    setup_routers(dispatcher)


def create_dispatcher(config: Config) -> Dispatcher:
    storage = RedisStorage.from_url(
        url=config.redis.dsn,
        key_builder=DefaultKeyBuilder(with_destiny=True),
        state_ttl=timedelta(days=1),
        data_ttl=timedelta(days=1),
    )
    event_isolation = RedisEventIsolation(
        storage.redis,
        UserIdKeyBuilder(),
    )
    redman = Redman(storage.redis)

    dispatcher = Dispatcher(storage=storage, events_isolation=event_isolation)
    dispatcher["config"] = config
    dispatcher["redman"] = redman

    dispatcher.startup.register(on_startup)

    return dispatcher
