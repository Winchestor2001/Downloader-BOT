from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import lang_callback

select_lang_btns = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 UZ", callback_data=lang_callback.new(lang='lang', val='uz')),
            InlineKeyboardButton(text="🇷🇺 RU", callback_data='language:lang:ru')
        ],
        [
            InlineKeyboardButton(text="🇹🇷 TR", callback_data='language:lang:tr'),
            InlineKeyboardButton(text="🇬🇧 EN", callback_data='language:lang:en')
        ]
    ]
)