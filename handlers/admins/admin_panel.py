import asyncio
import os

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.exceptions import BotBlocked, TelegramAPIError

from keyboards.default.cencel_btn import cencel_send_btn, remove
from keyboards.inline.admin_panel_btns import admin_panel
from keyboards.inline.channels_btn import add_channel_btn, add_admin_btn, send_post_btn, del_channel_btn, del_admin_btn
from loader import dp, bot
from database.connection import *
from aiogram.dispatcher.filters.builtin import Command
from data.config import ADMINS, user_bot_id
from states.admin_states import AdminStates
from aiogram.dispatcher import FSMContext

import sqlite3 as sql


@dp.message_handler(Command('admin'))
async def admin_panel_handler(message: Message):
    user_id = message.from_user.id
    admins_list = []
    today_date = datetime.datetime.now().strftime("%d/%m/%Y")

    with db:
        db_admins = Admins.select()
        users = Users.select().count()
        users_lang_uz = Users.select().where(Users.lang == 'uz').count()
        users_lang_ru = Users.select().where(Users.lang == 'ru').count()
        users_lang_tr = Users.select().where(Users.lang == 'tr').count()
        users_lang_en = Users.select().where(Users.lang == 'en').count()
        today_add_users = Users.select().where(Users.data == today_date).count()
        for da in db_admins:
            admins_list.append(str(da.admin_id))


    if str(user_id) in ADMINS or str(user_id) in admins_list:
        await message.answer(f"Siz admin paneldasiz:\n\n"
                             f"Bot a'zolari: <b>{users}</b> ta\n"
                             f"UZ: {users_lang_uz} ta\n"
                             f"RU: {users_lang_ru} ta\n"
                             f"TR: {users_lang_tr} ta\n"
                             f"EN: {users_lang_en} ta\n\n"
                             f"Bugun qushilgan a`zolar soni: {today_add_users} ta", reply_markup=admin_panel)


@dp.message_handler(Command('add_users'))
async def add_users_handler(message: Message):
    user_id = message.from_user.id
    admins_list = []

    with db:
        db_admins = Admins.select()
        for da in db_admins:
            admins_list.append(str(da.admin_id))

    if str(user_id) in ADMINS or str(user_id) in admins_list:
        with open('users.txt', 'r', encoding="utf-8") as f:
            lines = f.readlines()
        for users in lines:
            user = users.strip().split(':')
            with db:
                Users.insert(user_id=user[0], first_name=user[1],
                                       lang=user[2]).on_conflict(conflict_target=(Users.user_id,),
                                                              preserve=(Users.first_name,),
                                                              update={Users.user_id: user[0]}).execute()
            await asyncio.sleep(1)




@dp.callback_query_handler(text='del_panel')
async def del_panel_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    await c.message.delete()


@dp.callback_query_handler(text='back')
async def back_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    with db:
        users = Users.select().count()

    await c.message.edit_text(f"Siz admin paneldasiz:\n\n"
                         f"Bot a'zolari: <b>{users}</b> ta", reply_markup=admin_panel)



@dp.callback_query_handler(text='add_channel')
async def add_channel_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    user_id = c.from_user.id
    with db:
        channels = Channels.select()
    add_channel_btn.inline_keyboard.clear()

    achb_1 = InlineKeyboardButton("➕", callback_data="channel_config")
    achb_2 = InlineKeyboardButton("Ortga ↩️", callback_data="back")
    add_channel_btn.add(achb_1, achb_2)

    for row in channels:
        text = row.channel_name
        id = row.channel_id
        link = row.channel_link

        add_btn = InlineKeyboardButton(text, callback_data=id)
        add_channel_btn.add(add_btn)

    await bot.answer_callback_query(c.id)
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=c.message.message_id,
        text=f"📶 Kanallar ro`yxati:",
        reply_markup=add_channel_btn
    )
    add_channel_btn.inline_keyboard.clear()


@dp.callback_query_handler(text='channel_config')
async def channel_config_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    add_channel_btn.inline_keyboard.clear()
    add_channel_btn.add(InlineKeyboardButton("Ortga ↩️", callback_data="back"))

    await AdminStates.add_channel_check.set()

    await bot.answer_callback_query(c.id)
    await bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text='Kanal qushish uchun shu kurinishda yozing:\n\n<em>KANAL NOMI + KANAL ID + https://t.me/+9DejWHHYHVVkMzg6</em>',
        reply_markup=add_channel_btn,
        disable_web_page_preview=True
    )



@dp.callback_query_handler(text='add_admin')
async def add_admin_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    user_id = c.from_user.id
    with db:
        db_admins = Admins.select()

    add_admin_btn.inline_keyboard.clear()

    achb_1 = InlineKeyboardButton("➕", callback_data="admin_config")
    achb_2 = InlineKeyboardButton("Ortga ↩️", callback_data="back")
    add_admin_btn.add(achb_1, achb_2)

    for row in db_admins:
        text = row.admin_name
        id = row.admin_id

        add_btn = InlineKeyboardButton(text, callback_data=f"new_{id}")
        add_admin_btn.add(add_btn)

    await bot.answer_callback_query(c.id)
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=c.message.message_id,
        text=f"📶 Adminlar ro`yxati:",
        reply_markup=add_admin_btn
    )
    add_admin_btn.inline_keyboard.clear()



@dp.callback_query_handler(text='admin_config')
async def admin_config_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    add_admin_btn.inline_keyboard.clear()
    add_admin_btn.add(InlineKeyboardButton("Ortga ↩️", callback_data="back"))

    await AdminStates.add_admin_check.set()

    await bot.answer_callback_query(c.id)
    await bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text='Admin qushish uchun shu kurinishda yozing:\n\n<em>Admin Ismi + Admin IDsi</em>',
        reply_markup=add_admin_btn
    )



@dp.callback_query_handler(text='rek')
async def reklama_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    await AdminStates.send_message.set()
    await bot.delete_message(chat_id=c.message.chat.id, message_id=c.message.message_id)
    await c.message.answer(f"VIDEO, AUDIO, RASIM, MATN lardan birini yuboring.\n\n"
                                    f"Namuna 👇")
    await bot.send_photo(
        chat_id=c.from_user.id,
        photo="https://i.ytimg.com/vi/JFcFsIrI2fU/maxresdefault.jpg",
        caption=f"<em>MATIN (text)</em>\n\n<em>knopka nomi + t.me/xavola</em>",
        reply_markup=cencel_send_btn)



@dp.callback_query_handler(text_contains='delchannel')
async def del_channel_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    del_channel = c.data.split(':')[1]
    with db:
        Channels.delete().where(Channels.channel_id == del_channel).execute()
        channels = Channels.select()

    add_channel_btn.inline_keyboard.clear()
    achb_1 = InlineKeyboardButton("➕", callback_data="channel_config")
    achb_2 = InlineKeyboardButton("Ortga ↩️", callback_data="back")
    add_channel_btn.add(achb_1, achb_2)
    for row in channels:
        text = row.channel_name
        id = row.channel_id
        link = row.channel_link

        add_btn = InlineKeyboardButton(text, callback_data=id)
        add_channel_btn.add(add_btn)
    await c.message.edit_reply_markup(add_channel_btn)


@dp.callback_query_handler(text_contains='-100')
async def channel_info_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    del_link = f'delchannel:{c.data}'
    del_channel_btn.inline_keyboard.clear()
    await bot.answer_callback_query(c.id)
    dchb_1 = InlineKeyboardButton("Ortga ↩️", callback_data="back")
    dchb_2 = InlineKeyboardButton("❌", callback_data=f"{del_link}")
    del_channel_btn.add(dchb_1, dchb_2)

    with db:
        channel = Channels.select().where(Channels.channel_id == c.data)
    for row in channel:
        text = row.channel_name
        id = row.channel_id
        link = row.channel_link
        del_channel_btn.add(InlineKeyboardButton(text, url=link))
    await c.message.edit_reply_markup(del_channel_btn)



@dp.callback_query_handler(text_contains='new')
async def admin_info_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    spliting = c.data.split('_')
    del_link = f'deladmin_{spliting[1]}'
    del_admin_btn.inline_keyboard.clear()
    await bot.answer_callback_query(c.id)

    dchb_1 = InlineKeyboardButton("Ortga ↩️", callback_data="back")
    dchb_2 = InlineKeyboardButton("❌", callback_data=f"{del_link}")
    del_admin_btn.add(dchb_1, dchb_2)

    with db:
        channel = Admins.select().where(Admins.admin_id == int(spliting[1]))
    for row in channel:
        text = row.admin_name
        id = row.admin_id
        del_admin_btn.add(InlineKeyboardButton(text, callback_data="id"))

    await c.message.edit_reply_markup(del_admin_btn)
    # await bot.edit_message_text(
    #     chat_id=c.message.chat.id,
    #     message_id=c.message.message_id,
    #     text=f"📶 Adminlar ro'yxati:",
    #     reply_markup=del_admin_btn
    # )



@dp.callback_query_handler(text_contains='deladmin')
async def del_admin_handler(c: CallbackQuery):
    await c.answer(cache_time=5)
    del_adm = c.data.split('_')[1]
    with db:
        Admins.delete().where(Admins.admin_id == del_adm).execute()
        db_admins = Admins.select()

    add_admin_btn.inline_keyboard.clear()
    achb_1 = InlineKeyboardButton("➕", callback_data="admin_config")
    achb_2 = InlineKeyboardButton("Ortga ↩️", callback_data="back")
    add_admin_btn.add(achb_1, achb_2)
    for row in db_admins:
        text = row.admin_name
        id = row.admin_id

        add_btn = InlineKeyboardButton(text, callback_data=f"new_{id}")
        add_admin_btn.add(add_btn)

    await c.message.edit_reply_markup(add_admin_btn)




@dp.message_handler(content_types=['video'])
async def videos_save_to_db(message: Message):
    user_id = message.from_user.id
    BOT_NAME = await bot.get_me()

    if user_id == user_bot_id:
        video_id = message.video.file_id
        video_caption = message.caption

        title = video_caption.split("\n")[0]
        user = video_caption.split("\n")[1]
        await bot.send_video(user, video_id, caption=f"<em>{title}</em>\n\n<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Tez va oson yuklovchi bot!</b>",)

        with db:
            Youtube_Videos.get_or_create(video_name=title, video_id=video_id)
            VideosQueue.delete().where(VideosQueue.user_id == user).execute()







# ADMIN STATES
@dp.message_handler(state=AdminStates.add_channel_check)
async def add_channel_check_state(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.split(" + ")
    prefix = '-100'
    try:
        if len(text) == 3:
            name = text[0]
            id = text[1]
            link = text[2]

            if id.isdigit():
                bot_id = await bot.get_me()
                status = await bot.get_chat_member(chat_id=prefix + id, user_id=bot_id.id)

                if status.status != 'administrator':
                    await bot.send_message(message.chat.id, 'Meni oldin kanalda admin qiling !')

                else:
                    await bot.send_message(user_id, f"✅ Nomi: {name}\n"
                                                    f"✅ Link: {link}", disable_web_page_preview=True)

                    channel_id = prefix + id
                    with db:
                        Channels.get_or_create(channel_name=name, channel_id=channel_id, channel_link=link)
                        channels = Channels.select()

                    add_channel_btn.inline_keyboard.clear()
                    achb_1 = InlineKeyboardButton("➕", callback_data="channel_config")
                    achb_2 = InlineKeyboardButton("Ortga ↩️", callback_data="back")
                    add_channel_btn.add(achb_1, achb_2)
                    for row in channels:
                        text = row.channel_name
                        id = row.channel_id
                        link = row.channel_link

                        add_btn = InlineKeyboardButton(text, callback_data=id)
                        add_channel_btn.add(add_btn)

                    await bot.send_message(
                        chat_id=user_id,
                        text=f"📶 Kanallar ro'yxati:",
                        reply_markup=add_channel_btn
                    )
                await state.finish()

        else:
            await bot.send_message(user_id,
                                   'Kanal qushish uchun shu kurinishda yozing:\n\n<em>KANAL NOMI + KANAL ID + https://t.me/+9DejWHHYHVVkMzg6</em>',
                                   disable_web_page_preview=True, reply_markup=cencel_send_btn)

    except Exception:
        await bot.send_message(user_id, '<b>Kanal topilmadi!</b>')



@dp.message_handler(state=AdminStates.add_admin_check)
async def add_admin_check_state(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.split(" + ")
    add_admin_btn.inline_keyboard.clear()

    if len(text) == 2:
        name = text[0]
        id = text[1]

        if text[1].isdigit():
            await bot.send_message(user_id, f"✅ Admin Ismi: {name}\n"
                                            f"✅ Admin IDsi: {id}")

            with db:
                Admins.get_or_create(admin_id=id, admin_name=name)
                db_admins = Admins.select()

            achb_1 = InlineKeyboardButton("➕", callback_data="admin_config")
            achb_2 = InlineKeyboardButton("Ortga ↩️", callback_data="back")
            add_admin_btn.add(achb_1, achb_2)

            for row in db_admins:
                text = row.admin_name
                id = row.admin_id

                add_btn = InlineKeyboardButton(text, callback_data=f"new_{id}")
                add_admin_btn.add(add_btn)

            await bot.send_message(
                chat_id=user_id,
                text=f"📶 Adminlar ro'yxati:",
                reply_markup=add_admin_btn
            )
            add_admin_btn.inline_keyboard.clear()
            await state.finish()

    else:
        await bot.send_message(user_id,
                               'Admin qushish uchun shu kurinishda yozing:\n\n<em>Admin Ismi + Admin IDsi</em>')



@dp.message_handler(state=AdminStates.send_message, content_types=['text', 'photo', 'video', 'animation', 'document'])
async def send_message_state(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text_type = message.content_type
    text = message.text
    text_caption = message.html_text
    rep_btn = message.reply_markup
    if text == '❌':
        await bot.send_message(user_id, "❌", reply_markup=remove)
        await bot.send_message(user_id, f"Siz admin paneldasiz:", reply_markup=admin_panel)
        await state.finish()
    else:
        admins = []
        users = []
        with db:
            db_admins = Admins.select()
            userss = Users.select()
            for da in db_admins:
                admins.append(str(da.admin_id))
            for user in userss:
                users.append(user.user_id)

        if str(user_id) in ADMINS or str(user_id) in admins:
            sends = 0
            sends_error = 0
            send_post_btn.inline_keyboard.clear()
            await bot.send_message(user_id, "Xabarni yuborishni boshladim....", reply_markup=remove)
            await bot.send_message(user_id, f"Siz admin paneldasiz:", reply_markup=admin_panel)
            await state.finish()

            for u in users:
                try:
                    if text_type == 'text':
                        await bot.send_message(u, text, reply_markup=rep_btn)
                        sends += 1
                        await asyncio.sleep(0.5)

                    elif text_type == "photo":
                        await bot.send_photo(u, message.photo[-1].file_id, caption=text_caption,
                                             reply_markup=rep_btn)
                        sends += 1
                        await asyncio.sleep(0.5)

                    elif text_type == "video":
                        await bot.send_video(u, message.video.file_id, caption=text_caption,
                                             reply_markup=rep_btn)
                        sends += 1
                        await asyncio.sleep(0.5)

                    elif text_type == "animation":
                        await bot.send_animation(u, message.animation.file_id, caption=text_caption,
                                                 reply_markup=rep_btn)
                        sends += 1
                        await asyncio.sleep(0.5)

                    elif text_type == "document":
                        await bot.send_document(u, message.document.file_id, caption=text_caption,
                                                reply_markup=rep_btn)
                        sends += 1
                        await asyncio.sleep(0.5)



                except BotBlocked:
                    sends_error += 1
                    continue

                except TelegramAPIError:
                    await asyncio.sleep(0.3)
                    continue

                except Exception as ex:
                    sends_error += 1
                    print(ex)
                    continue

            if sends == 0:
                await bot.send_message(user_id, "⚠️ Xabar xechkimga etibormadi!")
            else:
                await bot.send_message(user_id,
                                       f"Siz yuborgan xabar <b>{sends}</b> ta a'zoga yetib bordi va <b>{sends_error}</b> ta a'zoga yetibormadi!")



