from aiogram.dispatcher.filters.state import StatesGroup, State





class AdminStates(StatesGroup):
    add_channel_check = State()
    send_message = State()
    add_admin_check = State()