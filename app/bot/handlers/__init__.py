from aiogram import Router

from app.bot.handlers import errors, start
from app.bot.handlers.profile import lang


def setup_routers(router: Router) -> None:
    router.include_routers(
        lang.router,
        start.router,
        errors.router,
    )
