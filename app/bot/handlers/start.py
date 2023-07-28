from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.bot.keyboards import Buttons
from app.bot.states import MortgageRequest
from app.services.fluent import I18n
from app.types import HandlerReturnType
from app.utils import is_first_amount_valid

router = Router(name=__name__)


@router.message(CommandStart())
async def process_start_command(
    message: types.Message,
    i18n: I18n,
    buttons: Buttons,
    state: FSMContext,
) -> HandlerReturnType:
    user = message.from_user
    await state.set_state(MortgageRequest.wait_credit_amount)
    return message.answer(
        i18n.command.start.text(user=user.full_name),
    )


@router.message(MortgageRequest.wait_credit_amount)
async def process_credit_amount(
    message: types.Message,
    i18n: I18n,
    buttons: Buttons,
    state: FSMContext,
) -> HandlerReturnType:
    credit_amount_raw = message.text.strip().replace(" ", "")
    if not credit_amount_raw.isdigit():
        return message.answer(i18n.command.digit_answer.failed())

    credit_amount = int(credit_amount_raw)

    await state.update_data(credit_amount=credit_amount)

    await state.set_state(MortgageRequest.wait_first_pay_amount)

    return message.answer(i18n.command.credit_amount.success())


@router.message(MortgageRequest.wait_first_pay_amount)
async def process_first_pay_amount(
    message: types.Message,
    i18n: I18n,
    buttons: Buttons,
    state: FSMContext,
) -> HandlerReturnType:
    first_pay_amount_raw = message.text.strip().replace(" ", "")

    data = await state.get_data()
    credit_amount = data["credit_amount"]

    if not first_pay_amount_raw.isdigit():
        return message.answer(i18n.command.digit_answer.failed())

    first_pay_amount = int(first_pay_amount_raw)

    if not is_first_amount_valid(first_pay_amount, credit_amount):
        return message.answer(i18n.command.first_pay_amount.invalid())

    return message.answer(
        i18n.command.first_pay_amount.success(),
        reply_markup=buttons.web_link(),
    )
