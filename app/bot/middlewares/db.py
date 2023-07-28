from aiogram import BaseMiddleware
from aiogram.types import Update, User

from app.services.db import UserRepo
from app.types import AsyncSessionMaker, Data, Handler, MiddlewareReturnType


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker: AsyncSessionMaker):
        super().__init__()
        self.session_maker = session_maker

    async def __call__(
        self, handler: Handler[Update], event: Update, data: Data
    ) -> MiddlewareReturnType:
        async with self.session_maker() as session:
            data["session"] = session
            data["user_repo"] = UserRepo(session)
            return await handler(event, data)


class SyncUserMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Handler[Update], event: Update, data: Data
    ) -> MiddlewareReturnType:
        user: User = data["event_from_user"]
        if not user.is_bot:
            user_repo: UserRepo = data["user_repo"]
            await user_repo.sync_user(user_id=user.id)

        return await handler(event, data)
