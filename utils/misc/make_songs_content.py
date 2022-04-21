from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import song_callback


async def songs_package_func(array):
    # for a in array:
    #     print(a)

    text = ''
    file_ids = []
    songs_ids = []
    result = []

    for n, s in enumerate(array, start=1):
        if n < 11:
            text += f"{n}. {s[2]} – {s[1]} {str(s[3])} {s[4]}\n"
            file_ids.append(s[0])
            songs_ids.append(f"{s[3]}_{s[2]}")
    result.append([text, file_ids, songs_ids])

# MAKE BTN
    songs_btn = InlineKeyboardMarkup(row_width=5)
    btns_list = []

    for n, i in enumerate(array, start=1):
        if n < 6:
            btns_list.append(InlineKeyboardButton(f"{n}", callback_data=song_callback.new(song='song', val=f"{i[0]}")))
        elif n > 5:
            btns_list.append(InlineKeyboardButton(f"{n}", callback_data=f"song_list:song:{i[0]}"))


    songs_btn.add(*btns_list)
    songs_btn.row(InlineKeyboardButton("❌", callback_data='remove_songs_tab'))
    result.append(songs_btn)

    return result