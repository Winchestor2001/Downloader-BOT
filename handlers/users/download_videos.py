import asyncio
import sys

from aiogram.utils.exceptions import MessageTextIsEmpty
from moviepy.video.io.VideoFileClip import VideoFileClip
from tiktok_downloader import snaptik, InvalidUrl

from keyboards.default.cencel_btn import remove
from keyboards.inline.admin_panel_btns import admin_panel
from keyboards.inline.channels_btn import channels_btn
from utils.misc.subscribe import channelsCheckFunc, showChannels
from utils.misc.tiktok_downloader import download_tiktok
from utils.misc.instagram_downloader import instagram_downloader
from utils.misc.check_lang import checkingUserLangFunc
from data.config import WORDS_PASS
import datetime
import os
import random
from pytube import YouTube

from aiogram.types import Message
from loader import dp, bot
from database.connection import *
from utils.user_bot.u_bot import get_large_video  # send_large_video


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
                                caption=f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Tez va oson yuklovchi bot!</b>",
                                reply_to_message_id=message.message_id
                            )
                        f_name = f'media/videos/{user_id}.mp4'
                        os.unlink(f_name)

                else:
                    snaptik(message.text).get_media()[0].download(f"media/videos/{message.from_user.id}.mp4")
                    await msg1.delete()
                    with open(f'media/videos/{message.from_user.id}.mp4', 'rb') as file:
                        await bot.send_video(
                            chat_id=message.chat.id,
                            video=file,
                            caption=f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Tez va oson yuklovchi bot!</b>",
                            reply_to_message_id=message.message_id
                        )
                    f_name = f'media/videos/{user_id}.mp4'
                    os.unlink(f_name)


            elif message.text.startswith('https://vm.tiktok.com') or message.text.startswith('http://vm.tiktok.com') or message.text.startswith('https://vt.tiktok.com'):
                try:
                    if len(snaptik(message.text).get_media()) == 0:
                        second_tik = await download_tiktok(user_id, message.text)
                        if second_tik:
                            await msg1.delete()
                            with open(f'media/videos/{message.from_user.id}.mp4', 'rb') as file:
                                await bot.send_video(
                                    chat_id=message.chat.id,
                                    video=file,
                                    caption=f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Tez va oson yuklovchi bot!</b>",
                                    reply_to_message_id=message.message_id
                                )
                            f_name = f'media/videos/{user_id}.mp4'
                            os.unlink(f_name)

                    else:
                        snaptik(message.text).get_media()[0].download(f"media/videos/{message.from_user.id}.mp4")
                        await msg1.delete()
                        with open(f'media/videos/{message.from_user.id}.mp4', 'rb') as file:
                            await bot.send_video(
                                chat_id=message.chat.id,
                                video=file,
                                caption=f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Tez va oson yuklovchi bot!</b>",
                                reply_to_message_id=message.message_id
                            )
                        f_name = f'media/videos/{user_id}.mp4'
                        os.unlink(f_name)

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
                            caption=f"<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Tez va oson yuklovchi bot!</b>",
                            reply_to_message_id=message.message_id
                        )
                    f_name = f'media/videos/{user_id}.mp4'
                    os.unlink(f_name)

                else:
                    await msg1.delete()
                    result = await checkingUserLangFunc(user_id, 'no_result')
                    await message.reply(result)


            elif message.text.startswith('https://youtu.be') or message.text.startswith('http://youtu.be') or message.text.startswith('https://youtube.com'):
                try:
                    youtube = YouTube(message.text)
                    video = youtube.streams.get_highest_resolution()
                    db_video = []

                    with db:
                        db_videos = Youtube_Videos.select().where(Youtube_Videos.video_name == video.title)
                        for dv in db_videos:
                            db_video.append(dv.video_name)
                            db_video.append(dv.video_id)

                    if db_videos:
                        await msg1.delete()
                        await bot.send_video(user_id, db_video[1], caption=f"<em>{db_video[0]}</em>\n\n<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Tez va oson yuklovchi bot!</b>", reply_to_message_id=message.message_id)

                    else:

                        if video.filesize < 49943729:
                            video.download('media/videos', filename=f"{user_id}.mp4")
                            f_name = f'media/videos/{user_id}.mp4'
                            await msg1.delete()
                            clip = VideoFileClip(f_name)
                            dur = int(clip.duration)
                            clip.close()
                            with open(f'{f_name}', 'rb') as file:
                                await bot.send_video(
                                    chat_id=message.chat.id,
                                    video=file,
                                    duration=dur,
                                    caption=f"<em>{video.title}</em>\n\n<b><a href='https://t.me/{BOT_NAME.username}'>{BOT_NAME.first_name}</a> - Tez va oson yuklovchi bot!</b>",
                                    reply_to_message_id=message.message_id
                                )
                            os.unlink(f_name)

                        else:
                            await msg1.delete()
                            result = await checkingUserLangFunc(user_id, 'uploading')
                            await message.answer(result)
                            msg_id = message.message_id - 1
                            title = video.title
                            video.download('media/videos', filename=f"{user_id}.mp4")
                            f_path = f'media/videos/{user_id}.mp4'
                            await get_large_video(f_path, user_id, title, msg_id)


                except Exception as ex:
                    result = await checkingUserLangFunc(user_id, 'please_wait')
                    await message.answer(result)
                    print(f'{type(ex).__name__}: {ex} | Line: {sys.exc_info()[-1].tb_lineno}')
                    # await bot.send_message(user_id='591250245', text=f'{type(ex).__name__}: {ex} | Line: {sys.exc_info()[-1].tb_lineno}')


            else:
                await bot.delete_message(user_id, message.message_id + 1)
                result = await checkingUserLangFunc(user_id, 'wrong_url')
                await message.answer(result)

        except MessageTextIsEmpty:
            result = await checkingUserLangFunc(user_id, 'no_result')
            await message.answer(result)

        except Exception as ex:
            result = await checkingUserLangFunc(user_id, 'no_result')
            await message.answer(result)
            print(f'{type(ex).__name__}: {ex} | Line: {sys.exc_info()[-1].tb_lineno}')

    else:
        user_lang = await checkingUserLangFunc(user_id=message.from_user.id, key='subscribe')
        await showChannels(message.from_user.id)
        await message.answer(user_lang, reply_markup=channels_btn)

