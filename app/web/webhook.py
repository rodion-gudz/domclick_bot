import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import TelegramMethod
from aiogram.types import Update
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import SecretStr

from app.config_reader import Config
from app.web.stubs import BotDI, DispatcherDI

router = APIRouter()
config = Config().webhook


@router.post(f"{config.path}")
async def handle_payok(
    update: Update,
    secret: SecretStr = Header(None, alias="X-Telegram-Bot-Api-Secret-Token"),
    dispatcher: Dispatcher = Depends(DispatcherDI),
    bot: Bot = Depends(BotDI),
):
    if (
        config.secret
        and config.secret.get_secret_value() != secret.get_secret_value()
    ):
        raise HTTPException(403, "Invalid secret")

    try:
        result = await dispatcher.feed_update(bot, update=update)
        if isinstance(result, TelegramMethod):
            await dispatcher.silent_call_request(bot, result)
    except Exception as e:
        logging.exception(e)

    return {"ok": True}
