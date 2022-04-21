from loader import bot

from database.connection import *
from utils.context import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def checkingUserLangFunc(user_id, key, first_name=None):
    with db:
        user_lang = Users.get(Users.user_id == user_id)

    if key == 'start':
            if user_lang.lang == 'uz':
                management = InlineKeyboardMarkup()
                management.row(InlineKeyboardButton("📄 Qo'llanma", callback_data="management"))

                text = f"<b>Assalomu alaykum {first_name}</b>\n\n" \
                       f"{welcome_uz}"
                return [text, management]

            elif user_lang.lang == 'ru':
                management = InlineKeyboardMarkup()
                management.row(InlineKeyboardButton("📄 Инструкция", callback_data="management"))

                text = f"<b>Привет {first_name}</b>\n\n" \
                       f"{welcome_ru}"
                return [text, management]

            elif user_lang.lang == 'tr':
                management = InlineKeyboardMarkup()
                management.row(InlineKeyboardButton("📄 Talimat", callback_data="management"))

                text = f"<b>Selamun aleykum {first_name}</b>\n\n" \
                       f"{welcome_tr}"
                return [text, management]


            elif user_lang.lang == 'en':
                management = InlineKeyboardMarkup()
                management.row(InlineKeyboardButton("📄 Instruction", callback_data="management"))

                text = f"<b>Hey {first_name}</b>\n\n" \
                       f"{welcome_en}"
                return [text, management]


    elif key == 'no_result':
            if user_lang.lang == 'uz':
                return no_result_uz

            elif user_lang.lang == 'ru':
                return no_result_ru

            elif user_lang.lang == 'tr':
                return no_result_tr

            elif user_lang.lang == 'en':
                return no_result_en


    elif key == 'lang':
            if user_lang.lang == 'uz':
                return select_lang_uz

            elif user_lang.lang == 'ru':
                return select_lang_ru

            elif user_lang.lang == 'tr':
                return select_lang_tr

            elif user_lang.lang == 'en':
                return select_lang_en


    elif key == 'limit':
            if user_lang.lang == 'uz':
                return mb_limit_uz

            elif user_lang.lang == 'ru':
                return mb_limit_ru

            elif user_lang.lang == 'tr':
                return mb_limit_tr

            elif user_lang.lang == 'en':
                return mb_limit_en


    elif key == 'subscribe':
        if user_lang.lang == 'uz':
            return subscrive_uz

        elif user_lang.lang == 'ru':
            return subscrive_ru

        elif user_lang.lang == 'tr':
            return subscrive_tr

        elif user_lang.lang == 'en':
            return subscrive_en


    elif key == 'wrong_url':
        if user_lang.lang == 'uz':
            return wrong_url_uz

        elif user_lang.lang == 'ru':
            return wrong_url_ru

        elif user_lang.lang == 'tr':
            return wrong_url_tr

        elif user_lang.lang == 'en':
            return wrong_url_en

