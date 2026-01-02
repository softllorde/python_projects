from aiogram.fsm.state import StatesGroup, State


class ClientStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_status_phone = State()
    waiting_for_status_value = State()
    waiting_for_status_choice = State()
    waiting_for_delete_phone = State()
    confirm_delete = State()
    