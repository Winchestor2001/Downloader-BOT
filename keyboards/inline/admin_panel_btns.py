from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data='add_channel'),
            InlineKeyboardButton(text="Xabar junatish 📮", callback_data='rek')
        ],

        [
            InlineKeyboardButton(text="➕ Admin qo'shish", callback_data='add_admin'),
            InlineKeyboardButton(text="Ortga ↩️", callback_data='del_panel')
        ]
    ]
)