from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    number = State()
    text = State()