from aiogram import F, Router, types
from aiogram.filters import Command

from app.bot.keyboards import Buttons, SetLang
from app.services.db import UserRepo
from app.services.fluent import I18n
from app.services.fluent.translator_hub import EscapedTranslatorHub
from app.types import HandlerReturnType

router = Router(name=__name__)


@router.message(Command("lang"), F.from_user)
async def process_lang_command(
    message: types.Message, i18n: I18n, buttons: Buttons
) -> HandlerReturnType:
    return message.reply(i18n.command.lang.text(), reply_markup=buttons.lang())


@router.callback_query(F.data == "lang", F.from_user)
async def process_lang_callback(
    call: types.CallbackQuery, i18n: I18n, buttons: Buttons
) -> HandlerReturnType:
    await call.message.answer(
        i18n.command.lang.text(), reply_markup=buttons.lang()
    )
    return call.answer()


@router.callback_query(SetLang.filter(), F.from_user)
async def process_set_lang_callback(
    call: types.CallbackQuery,
    user_repo: UserRepo,
    callback_data: SetLang,
    translator_hub: EscapedTranslatorHub,
) -> HandlerReturnType:
    await user_repo.set_user_lang(call.from_user.id, callback_data.lang)
    i18n = translator_hub.get_translator_by_locale(callback_data.lang)
    await call.message.edit_text(
        text=i18n.command.lang.changed(),
    )
    return call.answer()
