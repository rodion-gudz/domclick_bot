from aiogram.fsm.state import State, StatesGroup


class MortgageRequest(StatesGroup):
    wait_credit_amount = State()
    wait_first_pay_amount = State()
