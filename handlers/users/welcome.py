from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart, Command

from keyboards.inline.admin_panel_btns import admin_panel
from loader import dp, bot
from database.connection import *
from utils.misc.subscribe import channelsCheckFunc, showChannels
from keyboards.inline import channels_btn, select_lang_btns
from utils.misc.check_lang import checkingUserLangFunc
from utils.context import *
from keyboards.inline.callback_datas import lang_callback, song_callback


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    # await message.answer("Texnik ishlar olib borilyabti iltimos birozdang so`ng urinib kuring!")

    with db:
        result = (Users.insert(user_id=message.from_user.id, first_name=message.from_user.first_name, lang='no').on_conflict(conflict_target=(Users.user_id,),preserve=(Users.first_name,),update={Users.user_id: message.from_user.id}).execute())

    subscribe = await channelsCheckFunc(message.from_user.id)
    if subscribe:
        with db:
            lang = Users.get(Users.user_id == message.from_user.id)
            if lang.lang != 'no':
                user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='start', first_name=message.from_user.first_name)
                management = user_lang[1]
                await message.answer(user_lang[0], reply_markup=management)
            else:
                await message.answer(select_lang_uz, reply_markup=select_lang_btns.select_lang_btns)
    else:
        user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='subscribe')
        await showChannels(message.from_user.id)
        await message.answer(user_lang, reply_markup=channels_btn.channels_btn)



@dp.message_handler(Command('lang'))
async def change_lang(message: Message):
    # await message.answer("Texnik ishlar olib borilyabti iltimos birozdang so`ng urinib kuring!")
    user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='lang', first_name=message.from_user.first_name)
    await message.answer(user_lang, reply_markup=select_lang_btns.select_lang_btns)



@dp.callback_query_handler(lang_callback.filter(lang='lang'))
async def set_user_lang(c: CallbackQuery):
    await c.answer(cache_time=5)
    with db:
        lang = Users.get(Users.user_id == c.from_user.id)
        lang.lang = c.data.split(':')[-1]
        lang.save()

    user_lang = await checkingUserLangFunc(user_id=c.from_user.id, key='start', first_name=c.from_user.first_name)
    management = user_lang[1]
    await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=user_lang[0], reply_markup=management)


@dp.callback_query_handler(song_callback.filter(song='song'))
async def select_song(c: CallbackQuery, callback_data: dict):
    BOT_NAME = await bot.get_me()
    await c.answer(cache_time=5)
    with db:
        result = Songs_Db.get(Songs_Db.song_id == callback_data.get('val'))

        await bot.send_audio(c.from_user.id, result.song_token, caption=f"<b>{result.song_title} - {result.song_subtitle}</b>\n\n"
                                       f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>")


@dp.callback_query_handler(text='management')
async def send_instruction_video(c: CallbackQuery):
    user_id = c.from_user.id
    with db:
        user_lang = Users.get(Users.user_id == user_id)

    open_video = open("media/instruction.mp4", 'rb')
    BOT_NAME = await bot.get_me()

    if user_lang.lang == 'uz':
        video_caption = f"{video_caption_uz}<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>"
        await c.answer(cache_time=5)
        await bot.send_video(user_id, video=open_video,
                             caption=video_caption, reply_to_message_id=c.message.message_id)
        await c.message.edit_reply_markup()


    elif user_lang.lang == 'ru':
        video_caption = f"{video_caption_ru}<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Найдите нужную музыку быстро и легко!</b>"
        await c.answer(cache_time=5)
        await bot.send_video(user_id, video=open_video,
                             caption=video_caption, reply_to_message_id=c.message.message_id)
        await c.message.edit_reply_markup()


    elif user_lang.lang == 'tr':
        video_caption = f"{video_caption_tr}<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - İstediğiniz müziği hızlı ve kolay bir şekilde bulun!</b>"
        await c.answer(cache_time=5)
        await bot.send_video(user_id, video=open_video,
                             caption=video_caption, reply_to_message_id=c.message.message_id)
        await c.message.edit_reply_markup()


    elif user_lang.lang == 'en':
        video_caption = f"{video_caption_en}<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Find the music you want quickly and easily!</b>"
        await c.answer(cache_time=5)
        await bot.send_video(user_id, video=open_video,
                             caption=video_caption, reply_to_message_id=c.message.message_id)
        await c.message.edit_reply_markup()

    open_video.close()



@dp.callback_query_handler(text_contains='remove_songs_tab')
async def cancel_handler(c: CallbackQuery):
    await c.message.delete()


@dp.callback_query_handler(text_contains='del_panel')
async def del_panel_handler(c: CallbackQuery):
    await c.message.delete()



@dp.callback_query_handler(text='check_subscribe')
async def check_subscrive_handler(c: CallbackQuery):
    user_id = c.from_user.id

    subscribe = await channelsCheckFunc(c.from_user.id)
    if subscribe:
        user_lang = await checkingUserLangFunc(user_id=c.from_user.id, key='start', first_name=c.from_user.first_name)
        management = user_lang[1]
        await c.message.edit_text(user_lang[0], reply_markup=management)

    else:
        user_lang = await checkingUserLangFunc(user_id=c.from_user.id, key='subscribe')
        await showChannels(user_id)
        await bot.answer_callback_query(c.id, text=user_lang,show_alert=True)













