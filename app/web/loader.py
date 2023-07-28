from typing import Any

from fastapi import Depends, FastAPI

from app.bot import create_bot, create_dispatcher
from app.config_reader import Config
from app.web import payok, webhook
from app.web.stubs import (
    AsyncSessionMakerDI,
    BotDI,
    DispatcherDI,
    TranslatorHubDI,
)

app = FastAPI()
config = Config()

bot = create_bot(config)
dp = create_dispatcher(config)
workflow_data = {
    "app": app,
    "dispatcher": dp,
    **dp.workflow_data,
}

app.include_router(
    payok.router,
)
app.include_router(
    webhook.router,
)


def get_async_session_maker(dispatcher=Depends(DispatcherDI)):
    return dispatcher["session_maker"]


def get_translator_hub(dispatcher=Depends(DispatcherDI)):
    return dispatcher["translator_hub"]


app.dependency_overrides = {
    BotDI: lambda: bot,
    DispatcherDI: lambda: dp,
    AsyncSessionMakerDI: get_async_session_maker,
    TranslatorHubDI: get_translator_hub,
}


@app.on_event("startup")
async def on_startup(*_: Any, **__: Any) -> None:
    await dp.emit_startup(**workflow_data)


@app.on_event("shutdown")
async def on_shutdown(*_: Any, **__: Any) -> None:
    await dp.emit_shutdown(**workflow_data)
