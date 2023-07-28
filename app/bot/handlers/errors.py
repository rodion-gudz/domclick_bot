import logging

from aiogram import F, Router, types
from aiogram.types import ErrorEvent

from app.services.fluent import I18n
from app.types import HandlerReturnType

router = Router(name=__name__)


@router.errors(F.update.message.as_("message"))
async def process_errors(
    error: ErrorEvent, message: types.Message, i18n: I18n
) -> HandlerReturnType:
    logging.error(error.exception, exc_info=True)
