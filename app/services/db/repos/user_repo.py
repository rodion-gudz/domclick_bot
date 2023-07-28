from datetime import timedelta
from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.db.models import User

DEFAULT_TIME_LIMIT_IN_SECONDS = 24 * 60 * 60


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.delta = timedelta(seconds=DEFAULT_TIME_LIMIT_IN_SECONDS)

    async def sync_user(self, user_id: int) -> User:
        q = (
            insert(User)
            .values(id=user_id)
            .on_conflict_do_nothing()
            .returning(User)
        )

        async with self.session.begin():
            return await self.session.scalar(q)

    async def get_user(self, user_id: int) -> Optional[User]:
        q = select(User).where(User.id == user_id)

        async with self.session.begin():
            return await self.session.scalar(q)

    async def get_user_lang(
        self, user_id: int, default: Optional[str] = None
    ) -> str:
        q = select(User.lang).where(User.id == user_id)

        async with self.session.begin():
            return await self.session.scalar(q) or default

    async def set_user_lang(self, user_id: int, lang: str) -> None:
        q = update(User).where(User.id == user_id).values(lang=lang)

        async with self.session.begin():
            await self.session.execute(q)

    async def users_count(self) -> Optional[int]:
        q = select(func.count()).select_from(User)
        async with self.session.begin():
            return (await self.session.execute(q)).scalar()
