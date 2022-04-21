from loader import bot

from database.connection import *
from keyboards.inline.channels_btn import *




async def channelsCheckFunc(user_id):
    with db:
        channel_ids = Channels.select(Channels.channel_id)
        checked_list = []
        for ch in channel_ids:
            res = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if not res.is_chat_member():
                checked_list.append(False)
            else:
                checked_list.append(True)

        if False not in checked_list:
            return True

        else:
            return False



async def showChannels(user_id):
    with db:
        channels = Channels.select()
    channels_btn.inline_keyboard.clear()
    for row in channels:
        text = row.channel_name
        id = row.channel_id
        link = row.channel_link
        channel_id = id

        await bot.get_chat_member(channel_id, user_id,)

        chb = InlineKeyboardButton(text=text, url=link)
        channels_btn.add(chb)
    channels_btn.add(InlineKeyboardButton("✅ OBUNA BO'LDIM ✅", callback_data="check_subscribe"))

