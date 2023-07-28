from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update

from app.bot.keyboards import Buttons


class ButtonsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        data["buttons"] = Buttons(
            data["i18n"], data["config"], data["translator_hub"]
        )
        return await handler(event, data)
