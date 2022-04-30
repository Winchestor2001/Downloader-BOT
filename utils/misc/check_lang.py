from loader import bot

from database.connection import *
from utils.context import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def checkingUserLangFunc(user_id, key, first_name=None):
    try:
        user_lang = ''
        with db:
            for l in Users.select().where(Users.user_id == user_id):
                user_lang = l.lang

        if key == 'start':
                if user_lang == 'uz':
                    text = f"<b>Assalomu alaykum {first_name}</b>\n\n" \
                           f"{welcome_uz}"
                    return [text]

                elif user_lang == 'ru':
                    text = f"<b>Привет {first_name}</b>\n\n" \
                           f"{welcome_ru}"
                    return [text]

                elif user_lang == 'tr':
                    text = f"<b>Selamun aleykum {first_name}</b>\n\n" \
                           f"{welcome_tr}"
                    return [text]


                elif user_lang == 'en':
                    text = f"<b>Hey {first_name}</b>\n\n" \
                           f"{welcome_en}"
                    return [text]


        elif key == 'no_result':
                if user_lang == 'uz':
                    return no_result_uz

                elif user_lang == 'ru':
                    return no_result_ru

                elif user_lang == 'tr':
                    return no_result_tr

                elif user_lang == 'en':
                    return no_result_en


        elif key == 'lang':
                if user_lang == 'uz':
                    return select_lang_uz

                elif user_lang == 'ru':
                    return select_lang_ru

                elif user_lang == 'tr':
                    return select_lang_tr

                elif user_lang == 'en':
                    return select_lang_en


        elif key == 'limit':
                if user_lang == 'uz':
                    return mb_limit_uz

                elif user_lang == 'ru':
                    return mb_limit_ru

                elif user_lang == 'tr':
                    return mb_limit_tr

                elif user_lang == 'en':
                    return mb_limit_en


        elif key == 'subscribe':
            if user_lang == 'uz':
                return subscrive_uz

            elif user_lang == 'ru':
                return subscrive_ru

            elif user_lang == 'tr':
                return subscrive_tr

            elif user_lang == 'en':
                return subscrive_en


        elif key == 'wrong_url':
            if user_lang == 'uz':
                return wrong_url_uz

            elif user_lang == 'ru':
                return wrong_url_ru

            elif user_lang == 'tr':
                return wrong_url_tr

            elif user_lang == 'en':
                return wrong_url_en


        elif key == 'please_wait':
            if user_lang == 'uz':
                return please_wait_uz

            elif user_lang == 'ru':
                return please_wait_ru

            elif user_lang == 'tr':
                return please_wait_tr

            elif user_lang == 'en':
                return please_wait_en


        elif key == 'uploading':
            if user_lang == 'uz':
                return uploading_video_uz

            elif user_lang == 'ru':
                return uploading_video_ru

            elif user_lang == 'tr':
                return uploading_video_tr

            elif user_lang == 'en':
                return uploading_video_en

    except Exception:
        pass