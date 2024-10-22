from aiogram.fsm.state import StatesGroup, State


class SenderMsg(StatesGroup):
    text = State()
    media_type = State()
    media = State()
    btn_text = State()
    btn_url = State()
    confirm = State()


class AddMsg(StatesGroup):
    type = State()
    content = State()