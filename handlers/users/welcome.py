from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart, Command

from keyboards.inline.admin_panel_btns import admin_panel
from loader import dp, bot
from database.connection import *
from utils.misc.subscribe import channelsCheckFunc, showChannels
from keyboards.inline import channels_btn, select_lang_btns
from utils.misc.check_lang import checkingUserLangFunc
from utils.context import *
from keyboards.inline.callback_datas import lang_callback
import datetime


@dp.message_handler(commands=['start'])
async def bot_start(message: Message):
    # await message.answer("Texnik ishlar olib borilyabti iltimos birozdang so`ng urinib kuring!")
    try:
        with db:
            # Users.get_or_create(user_id=message.from_user.id, first_name=message.from_user.first_name, lang='no', data=str(datetime.datetime.now().strftime("%d/%m/%Y")))
            Users.insert(user_id=message.from_user.id, first_name=message.from_user.first_name, lang='uz', data=str(datetime.datetime.now().strftime("%d/%m/%Y"))).on_conflict(
                conflict_target=(Users.user_id,), preserve=(Users.data,),
                update={Users.user_id: message.from_user.id}).execute()
        subscribe = await channelsCheckFunc(message.from_user.id)
        if subscribe:
            lang = ''
            with db:
                for l in Users.select().where(Users.user_id == message.from_user.id):
                    lang = l.lang
            if lang != 'no':
                user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='start', first_name=message.from_user.first_name)
                await message.answer(user_lang[0])
            else:
                await message.answer(select_lang_uz, reply_markup=select_lang_btns.select_lang_btns)
        else:
            user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='subscribe')
            await showChannels(message.from_user.id)
            await message.answer(user_lang, reply_markup=channels_btn.channels_btn)
    except Exception as e:
        print(e)
        # pass


@dp.message_handler(commands=['lang'])
async def change_lang(message: Message):
    # await message.answer("Texnik ishlar olib borilyabti iltimos birozdang so`ng urinib kuring!")
    user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='lang', first_name=message.from_user.first_name)
    await message.answer(user_lang, reply_markup=select_lang_btns.select_lang_btns)



@dp.callback_query_handler(lang_callback.filter(lang='lang'))
async def set_user_lang(c: CallbackQuery):
    await c.answer(cache_time=5)
    try:
        with db:
            lang = Users.get(Users.user_id == c.from_user.id)
            lang.lang = c.data.split(':')[-1]
            lang.save()

        user_lang = await checkingUserLangFunc(user_id=c.from_user.id, key='start', first_name=c.from_user.first_name)
        management = user_lang[1]
        await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=user_lang[0])
    except:
        pass

# @dp.callback_query_handler(text='management')
# async def send_instruction_video(c: CallbackQuery):
#     user_id = c.from_user.id
#     with db:
#         user_lang = Users.get(Users.user_id == user_id)
#
#     open_video = open("media/instruction.mp4", 'rb')
#     BOT_NAME = await bot.get_me()
#
#     if user_lang.lang == 'uz':
#         video_caption = f"{video_caption_uz}<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>"
#         await c.answer(cache_time=5)
#         await bot.send_video(user_id, video=open_video,
#                              caption=video_caption, reply_to_message_id=c.message.message_id)
#         await c.message.edit_reply_markup()
#
#
#     elif user_lang.lang == 'ru':
#         video_caption = f"{video_caption_ru}<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Найдите нужную музыку быстро и легко!</b>"
#         await c.answer(cache_time=5)
#         await bot.send_video(user_id, video=open_video,
#                              caption=video_caption, reply_to_message_id=c.message.message_id)
#         await c.message.edit_reply_markup()
#
#
#     elif user_lang.lang == 'tr':
#         video_caption = f"{video_caption_tr}<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - İstediğiniz müziği hızlı ve kolay bir şekilde bulun!</b>"
#         await c.answer(cache_time=5)
#         await bot.send_video(user_id, video=open_video,
#                              caption=video_caption, reply_to_message_id=c.message.message_id)
#         await c.message.edit_reply_markup()
#
#
#     elif user_lang.lang == 'en':
#         video_caption = f"{video_caption_en}<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Find the music you want quickly and easily!</b>"
#         await c.answer(cache_time=5)
#         await bot.send_video(user_id, video=open_video,
#                              caption=video_caption, reply_to_message_id=c.message.message_id)
#         await c.message.edit_reply_markup()
#
#     open_video.close()


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













