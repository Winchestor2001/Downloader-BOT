from aiogram.utils.exceptions import MessageTextIsEmpty
from tiktok_downloader import snaptik, InvalidUrl

from keyboards.default.cencel_btn import remove
from keyboards.inline.admin_panel_btns import admin_panel
from keyboards.inline.channels_btn import channels_btn
from utils.misc.convert_file_size import convert_size
from utils.misc.make_songs_content import songs_package_func
from utils.misc.subscribe import channelsCheckFunc, showChannels
from utils.misc.tiktok_downloader import download_tiktok
from utils.misc.instagram_downloader import instagram_downloader
from utils.misc.shazam_listen import workWithShazam
from utils.misc.check_lang import checkingUserLangFunc
from data.config import WORDS_PASS
import datetime
import os
import random

from aiogram.types import Message
from loader import dp, bot
from database.connection import *



# @dp.message_handler(content_types=['text', 'photo', 'video', 'voice', 'audio'])
# async def texnik(message: Message):
#     await message.answer("Texnik ishlar olib borilyabti iltimos birozdang so`ng urinib kuring!")


@dp.message_handler(content_types=['text'])
async def text_handler(message: Message):
    user_id = message.from_user.id
    BOT_NAME = await bot.get_me()
    song_token = ''
    subscribe = await channelsCheckFunc(message.from_user.id)
    if subscribe:
        msg1 = await message.answer("🔎")

        try:
            if message.text.startswith('https://www.tiktok.com'):
                if len(snaptik(message.text).get_media()) == 0:
                    second_tik = await download_tiktok(user_id, message.text)
                    if second_tik:
                        await msg1.delete()
                        with open(f'media/videos/{message.from_user.id}.mp4', 'rb') as file:
                            await bot.send_video(
                                chat_id=message.chat.id,
                                video=file,
                                caption='Ushbu video musiqasi qidirilmoqda 🔎\n\n' \
                                        f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                reply_to_message_id=message.message_id
                            )
                        f_name = f'media/videos/{user_id}.mp4'
                        shazaming = await workWithShazam(f_name)
                        os.unlink(f_name)
                        if shazaming[0] == 'false':
                            result = await checkingUserLangFunc(user_id, 'no_result')
                            await message.reply(result)
                        else:
                            if shazaming[2] != 'false':
                                text = ""
                                for t in shazaming[2]:
                                    text += f"{t}\n"

                                if len(text) > 4096:
                                    for x in range(0, len(text), 4096):
                                        await bot.send_message(message.chat.id, text[x:x + 4096])
                                else:
                                    await bot.send_message(message.chat.id, text)

                            if shazaming[0] != 'false':
                                await bot.send_message(user_id,
                                                       f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                       f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                       disable_web_page_preview=True,
                                                       reply_to_message_id=message.message_id)

                                with db:
                                    result = Songs_Db.select().where(Songs_Db.song_title.contains(shazaming[0][0]) & Songs_Db.song_subtitle.contains(shazaming[0][1]))
                                    for i in result:
                                        song_token = i.song_token

                                if song_token != '':
                                    await bot.send_audio(user_id, f"{song_token}",
                                                         caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                                 f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                         reply_to_message_id=message.message_id)

                                else:
                                    if shazaming[1] != 'false':
                                        with open(shazaming[1], 'rb') as a:
                                            await bot.send_audio(user_id, a,
                                                                 caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                                         f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                                 reply_to_message_id=message.message_id,
                                                                 title=shazaming[0][1],
                                                                 performer=shazaming[0][0])
                                        os.remove(shazaming[1])
                else:
                    snaptik(message.text).get_media()[0].download(f"media/videos/{message.from_user.id}.mp4")
                    await msg1.delete()
                    with open(f'media/videos/{message.from_user.id}.mp4', 'rb') as file:
                        await bot.send_video(
                            chat_id=message.chat.id,
                            video=file,
                            caption='Ushbu video musiqasi qidirilmoqda 🔎\n\n' \
                                    f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                            reply_to_message_id=message.message_id
                        )
                    f_name = f'media/videos/{user_id}.mp4'
                    shazaming = await workWithShazam(f_name)
                    os.unlink(f_name)
                    os.remove(f_name)
                    if shazaming[0] == 'false':
                        result = await checkingUserLangFunc(user_id, 'no_result')
                        await message.reply(result)
                    else:
                        if shazaming[2] != 'false':
                            text = ""
                            for t in shazaming[2]:
                                text += f"{t}\n"

                            if len(text) > 4096:
                                for x in range(0, len(text), 4096):
                                    await bot.send_message(message.chat.id, text[x:x + 4096])
                            else:
                                await bot.send_message(message.chat.id, text)

                        if shazaming[0] != 'false':
                            await bot.send_message(user_id,
                                                   f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                   f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                   disable_web_page_preview=True,
                                                   reply_to_message_id=message.message_id)

                            with db:
                                result = Songs_Db.select().where(
                                    Songs_Db.song_title.contains(shazaming[0][0]) & Songs_Db.song_subtitle.contains(
                                        shazaming[0][1]))
                                for i in result:
                                    song_token = i.song_token

                            if song_token != '':
                                await bot.send_audio(user_id, f"{song_token}",
                                                     caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                             f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                     reply_to_message_id=message.message_id)

                            else:
                                if shazaming[1] != 'false':
                                    with open(shazaming[1], 'rb') as a:
                                        await bot.send_audio(user_id, a,
                                                             caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                                     f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                             reply_to_message_id=message.message_id,
                                                             title=shazaming[0][1],
                                                             performer=shazaming[0][0])
                                    os.remove(shazaming[1])


            elif message.text.startswith('https://vm.tiktok.com') or message.text.startswith('http://vm.tiktok.com'):
                try:
                    if len(snaptik(message.text).get_media()) == 0:
                        second_tik = await download_tiktok(user_id, message.text)
                        if second_tik:
                            await msg1.delete()
                            with open(f'media/videos/{message.from_user.id}.mp4', 'rb') as file:
                                await bot.send_video(
                                    chat_id=message.chat.id,
                                    video=file,
                                    caption='Ushbu video musiqasi qidirilmoqda 🔎\n\n' \
                                            f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                    reply_to_message_id=message.message_id
                                )
                            f_name = f'media/videos/{user_id}.mp4'
                            shazaming = await workWithShazam(f_name)
                            os.unlink(f_name)
                            if shazaming[0] == 'false':
                                result = await checkingUserLangFunc(user_id, 'no_result')
                                await message.reply(result)
                            else:
                                if shazaming[2] != 'false':
                                    text = ""
                                    for t in shazaming[2]:
                                        text += f"{t}\n"

                                    if len(text) > 4096:
                                        for x in range(0, len(text), 4096):
                                            await bot.send_message(message.chat.id, text[x:x + 4096])
                                    else:
                                        await bot.send_message(message.chat.id, text)

                                if shazaming[0] != 'false':
                                    await bot.send_message(user_id,
                                                           f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                           f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                           disable_web_page_preview=True,
                                                           reply_to_message_id=message.message_id)

                                    with db:
                                        result = Songs_Db.select().where(
                                            Songs_Db.song_title.contains(shazaming[0][0]) & Songs_Db.song_subtitle.contains(
                                                shazaming[0][1]))
                                        for i in result:
                                            song_token = i.song_token

                                    if song_token != '':
                                        await bot.send_audio(user_id, f"{song_token}",
                                                             caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                                     f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                             reply_to_message_id=message.message_id)

                                    else:
                                        if shazaming[1] != 'false':
                                            with open(shazaming[1], 'rb') as a:
                                                await bot.send_audio(user_id, a,
                                                                     caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                                             f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                                     reply_to_message_id=message.message_id,
                                                                     title=shazaming[0][1],
                                                                     performer=shazaming[0][0])
                                            os.remove(shazaming[1])
                    else:
                        snaptik(message.text).get_media()[0].download(f"media/videos/{message.from_user.id}.mp4")
                        await msg1.delete()
                        with open(f'media/videos/{message.from_user.id}.mp4', 'rb') as file:
                            await bot.send_video(
                                chat_id=message.chat.id,
                                video=file,
                                caption='Ushbu video musiqasi qidirilmoqda 🔎\n\n' \
                                        f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                reply_to_message_id=message.message_id
                            )
                        f_name = f'media/videos/{user_id}.mp4'
                        shazaming = await workWithShazam(f_name)
                        os.unlink(f_name)
                        if shazaming[0] == 'false':
                            result = await checkingUserLangFunc(user_id, 'no_result')
                            await message.reply(result)
                        else:
                            if shazaming[2] != 'false':
                                text = ""
                                for t in shazaming[2]:
                                    text += f"{t}\n"

                                if len(text) > 4096:
                                    for x in range(0, len(text), 4096):
                                        await bot.send_message(message.chat.id, text[x:x + 4096])
                                else:
                                    await bot.send_message(message.chat.id, text)

                            if shazaming[0] != 'false':
                                await bot.send_message(user_id,
                                                       f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                       f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                       disable_web_page_preview=True,
                                                       reply_to_message_id=message.message_id)

                                with db:
                                    result = Songs_Db.select().where(
                                        Songs_Db.song_title.contains(shazaming[0][0]) & Songs_Db.song_subtitle.contains(
                                            shazaming[0][1]))
                                    for i in result:
                                        song_token = i.song_token

                                if song_token != '':
                                    await bot.send_audio(user_id, f"{song_token}",
                                                         caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                                 f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                         reply_to_message_id=message.message_id)

                                else:
                                    if shazaming[1] != 'false':
                                        with open(shazaming[1], 'rb') as a:
                                            await bot.send_audio(user_id, a,
                                                                 caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                                         f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                                 reply_to_message_id=message.message_id,
                                                                 title=shazaming[0][1],
                                                                 performer=shazaming[0][0])
                                        os.remove(shazaming[1])

                except InvalidUrl:
                    await msg1.delete()
                    result = await checkingUserLangFunc(user_id, 'wrong_url')
                    await message.reply(result)


            elif message.text.startswith('https://www.instagram.com') or message.text.startswith('http://www.instagram.com'):
                sending_video = await instagram_downloader(user_id, message.text)
                if sending_video != 'false':
                    await msg1.delete()
                    with open(f'{sending_video}', 'rb') as file:
                        await bot.send_video(
                            chat_id=message.chat.id,
                            video=file,
                            caption='Ushbu video musiqasi qidirilmoqda 🔎\n\n' \
                                    f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                            reply_to_message_id=message.message_id
                        )
                    f_name = f'media/videos/{user_id}.mp4'
                    shazaming = await workWithShazam(f_name)
                    os.unlink(f_name)
                    if shazaming[0] == 'false':
                        result = await checkingUserLangFunc(user_id, 'no_result')
                        await message.reply(result)
                    else:
                        if shazaming[2] != 'false':
                            text = ""
                            for t in shazaming[2]:
                                text += f"{t}\n"

                            if len(text) > 4096:
                                for x in range(0, len(text), 4096):
                                    await bot.send_message(message.chat.id, text[x:x + 4096])
                            else:
                                await bot.send_message(message.chat.id, text)

                        if shazaming[0] != 'false':
                            await bot.send_message(user_id, f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                            f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                   disable_web_page_preview=True,
                                                   reply_to_message_id=message.message_id)

                            with db:
                                result = Songs_Db.select().where(
                                    Songs_Db.song_title.contains(shazaming[0][0]) & Songs_Db.song_subtitle.contains(
                                        shazaming[0][1]))
                                for i in result:
                                    song_token = i.song_token

                            if song_token != '':
                                await bot.send_audio(user_id, f"{song_token}",
                                                     caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                             f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                     reply_to_message_id=message.message_id)

                            else:
                                if shazaming[1] != 'false':
                                    with open(shazaming[1], 'rb') as a:
                                        await bot.send_audio(user_id, a,
                                                             caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                                     f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                             reply_to_message_id=message.message_id,
                                                             title=shazaming[0][1],
                                                             performer=shazaming[0][0])
                                    os.remove(shazaming[1])

                else:
                    await msg1.delete()
                    result = await checkingUserLangFunc(user_id, 'no_result')
                    await message.reply(result)


            else:
                await msg1.delete()
                songs_list = []
                with db:
                    result1 = Songs_Db.select().where(Songs_Db.song_title.contains(message.text)).limit(5)
                    result2 = Songs_Db.select().where(Songs_Db.song_subtitle.contains(message.text)).limit(5)
                    for i in result1:
                        songs_list.append([i.song_id, i.song_title, i.song_subtitle, i.song_size, i.song_duration])
                    for i in result2:
                        songs_list.append([i.song_id, i.song_title, i.song_subtitle, i.song_size, i.song_duration])


                result = await songs_package_func(songs_list)
                await message.answer(result[0][0], reply_markup=result[1])


        except MessageTextIsEmpty:
            result = await checkingUserLangFunc(user_id, 'no_result')
            await message.answer(result)
    else:
        user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='subscribe')
        await showChannels(message.from_user.id)
        await message.answer(user_lang, reply_markup=channels_btn)



@dp.message_handler(content_types=['video'])
async def video_handler(message: Message):
    user_id = message.from_user.id
    BOT_NAME = await bot.get_me()
    song_token = ''
    subscribe = await channelsCheckFunc(message.from_user.id)
    if subscribe:
        msg1 = await message.answer("🔎")

        if message.video.file_size > 5888888:
            await msg1.delete()
            result = await checkingUserLangFunc(user_id, 'limit')
            await message.reply(result)
        else:
            video = message.video.file_id
            video_file = await bot.get_file(video)
            path = video_file.file_path
            f_name = f'media/videos/{user_id}.mp4'
            await bot.download_file(path, f_name)
            shazaming = await workWithShazam(f_name)
            os.unlink(f_name)
            await msg1.delete()
            if shazaming[0] == 'false':
                result = await checkingUserLangFunc(user_id, 'no_result')
                await message.reply(result)
            else:
                if shazaming[2] != 'false':
                    text = ""
                    for t in shazaming[2]:
                        text += f"{t}\n"

                    if len(text) > 4096:
                        for x in range(0, len(text), 4096):
                            await bot.send_message(message.chat.id, text[x:x + 4096])
                    else:
                        await bot.send_message(message.chat.id, text)

                if shazaming[0] != 'false':
                    await bot.send_message(user_id,
                                           f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                           f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                           disable_web_page_preview=True,
                                           reply_to_message_id=message.message_id)

                    with db:
                        result = Songs_Db.select().where(
                            Songs_Db.song_title.contains(shazaming[0][0]) & Songs_Db.song_subtitle.contains(
                                shazaming[0][1]))
                        for i in result:
                            song_token = i.song_token

                    if song_token != '':
                        await bot.send_audio(user_id, f"{song_token}",
                                             caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                     f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                             reply_to_message_id=message.message_id)

                    else:
                        if shazaming[1] != 'false':
                            with open(shazaming[1], 'rb') as a:
                                await bot.send_audio(user_id, a,
                                                     caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                             f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                     reply_to_message_id=message.message_id,
                                                     title=shazaming[0][1],
                                                     performer=shazaming[0][0])
                            os.remove(shazaming[1])

    else:
        user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='subscribe')
        await showChannels(message.from_user.id)
        await message.answer(user_lang, reply_markup=channels_btn)



@dp.message_handler(content_types=['voice'])
async def voice_handler(message: Message):
    user_id = message.from_user.id
    BOT_NAME = await bot.get_me()
    song_token = ''
    subscribe = await channelsCheckFunc(message.from_user.id)
    if subscribe:
        msg1 = await message.answer("🔎")

        voice = message.voice.file_id
        voice_file = await bot.get_file(voice)
        path = voice_file.file_path
        f_name = f'media/voices/{user_id}.ogg'
        await bot.download_file(path, f_name)
        shazaming = await workWithShazam(f_name)
        os.unlink(f_name)
        await msg1.delete()
        if shazaming[0] == 'false':
            result = await checkingUserLangFunc(user_id, 'no_result')
            await message.reply(result)
        else:
            if shazaming[2] != 'false':
                text = ""
                for t in shazaming[2]:
                    text += f"{t}\n"

                if len(text) > 4096:
                    for x in range(0, len(text), 4096):
                        await bot.send_message(message.chat.id, text[x:x + 4096])
                else:
                    await bot.send_message(message.chat.id, text)

            if shazaming[0] != 'false':
                await bot.send_message(user_id,
                                       f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                       f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                       disable_web_page_preview=True,
                                       reply_to_message_id=message.message_id)

                with db:
                    result = Songs_Db.select().where(
                        Songs_Db.song_title.contains(shazaming[0][0]) & Songs_Db.song_subtitle.contains(
                            shazaming[0][1]))
                    for i in result:
                        song_token = i.song_token

                if song_token != '':
                    await bot.send_audio(user_id, f"{song_token}",
                                         caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                 f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                         reply_to_message_id=message.message_id)

                else:
                    if shazaming[1] != 'false':
                        with open(shazaming[1], 'rb') as a:
                            await bot.send_audio(user_id, a,
                                                 caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                         f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                 reply_to_message_id=message.message_id,
                                                 title=shazaming[0][1],
                                                 performer=shazaming[0][0])
                        os.remove(shazaming[1])

    else:
        user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='subscribe')
        await showChannels(message.from_user.id)
        await message.answer(user_lang, reply_markup=channels_btn)




@dp.message_handler(content_types=['audio'])
async def audio_handler(message: Message):
    user_id = message.from_user.id
    BOT_NAME = await bot.get_me()
    song_token = ''
    random_token = ''
    senders = [1635543672, 5062203651]

    if user_id in senders:
        for i in range(0, 20):
            random_token += random.choice(WORDS_PASS)
        file_size = await convert_size(message.audio.file_size)
        time_dur = datetime.timedelta(seconds=int(message.audio.duration))
        f_title = message.audio.title
        f_performer = message.audio.performer
        f_name = message.audio.file_name

        with db:
            if f_title is None or f_performer is None:
                Songs_Db.create(song_id=random_token, song_token=message.audio.file_id, song_title=f_name.strip(), song_size=f"{file_size}", song_duration=str(time_dur)[2:])
            else:
                Songs_Db.create(song_id=random_token, song_token=message.audio.file_id, song_title=f_title.strip(), song_subtitle=f_performer.strip(), song_size=f"{file_size}", song_duration=str(time_dur)[2:])
        await message.answer('✅ SAVED ✅')


    else:
        subscribe = await channelsCheckFunc(message.from_user.id)
        if subscribe:
            msg1 = await message.answer("🔎")
            if message.audio.file_size > 5888888:
                await msg1.delete()
                result = await checkingUserLangFunc(user_id, 'limit')
                await message.reply(result)
            else:
                audio = message.audio.file_id
                audio_file = await bot.get_file(audio)
                path = audio_file.file_path
                f_name = f'media/audios/{user_id}.mp4'
                await bot.download_file(path, f_name)
                shazaming = await workWithShazam(f_name)
                os.unlink(f_name)
                await msg1.delete()
                if shazaming[0] == 'false':
                    result = await checkingUserLangFunc(user_id, 'no_result')
                    await message.reply(result)
                else:
                    if shazaming[2] != 'false':
                        text = ""
                        for t in shazaming[2]:
                            text += f"{t}\n"

                        if len(text) > 4096:
                            for x in range(0, len(text), 4096):
                                await bot.send_message(message.chat.id, text[x:x + 4096])
                        else:
                            await bot.send_message(message.chat.id, text)

                    if shazaming[0] != 'false':
                        await bot.send_message(user_id,
                                               f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                               f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                               disable_web_page_preview=True,
                                               reply_to_message_id=message.message_id)

                        with db:
                            result = Songs_Db.select().where(
                                Songs_Db.song_title.contains(shazaming[0][0]) & Songs_Db.song_subtitle.contains(
                                    shazaming[0][1]))
                            for i in result:
                                song_token = i.song_token

                        if song_token != '':
                            await bot.send_audio(user_id, f"{song_token}",
                                                 caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                         f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                 reply_to_message_id=message.message_id)

                        else:
                            if shazaming[1] != 'false':
                                with open(shazaming[1], 'rb') as a:
                                    await bot.send_audio(user_id, a,
                                                         caption=f"<b>{shazaming[0][1]} - {shazaming[0][0]}</b>\n\n"
                                                                 f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Istagan musiqangizni tez va oson toping!</b>",
                                                         reply_to_message_id=message.message_id,
                                                         title=shazaming[0][1],
                                                         performer=shazaming[0][0])
                                os.remove(shazaming[1])
        else:
            user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='subscribe')
            await showChannels(message.from_user.id)
            await message.answer(user_lang, reply_markup=channels_btn)