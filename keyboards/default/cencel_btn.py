from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton



remove = ReplyKeyboardRemove()


cencel_send_btn = ReplyKeyboardMarkup(resize_keyboard=True)
cencel_send_btn.add(KeyboardButton("❌"))


