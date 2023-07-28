from aiogram import BaseMiddleware
from aiogram.types import Update, User

from app.services.db import UserRepo
from app.services.fluent.translator_hub import EscapedTranslatorHub
from app.types import Data, Handler, MiddlewareReturnType


class I18nMiddleware(BaseMiddleware):
    def __init__(self, translator_hub: EscapedTranslatorHub):
        super().__init__()
        self.translator_hub = translator_hub

    async def __call__(
        self, handler: Handler[Update], event: Update, data: Data
    ) -> MiddlewareReturnType:
        user: User = data["event_from_user"]
        user_repo: UserRepo = data["user_repo"]

        data["i18n"] = self.translator_hub.get_translator_by_locale(
            await user_repo.get_user_lang(
                user_id=user.id, default=user.language_code
            )
        )
        return await handler(event, data)
