import os
import sys
import time

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon.tl.types import DocumentAttributeVideo
from telethon import TelegramClient, errors
import asyncio
from moviepy.video.io.VideoFileClip import VideoFileClip
from aiogram.bot.api import TelegramAPIServer
from aiogram import Bot, Dispatcher, executor, types
import logging
from database.connection import *

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

name = 'anon'
api_id = 12083236
api_hash = "58f190be15abc1338f2de30d06b679d3"
bot_link = '@poiskmuzikabot'

client = TelegramClient(name, api_id, api_hash)
client.start()


async def send_large_video():
    data = []
    try:
        with db:
            for v in VideosQueue.select():
                data.append(v.file_path)
                data.append(v.title)
                data.append(v.user_id)
                data.append(v.duration)
                data.append(v.post_id)
        bl = await client.get_entity(bot_link)
        await client.send_file(bl.id, file=f'videos/{data[2]}.mp4', caption=f"{data[1]}\n{data[2]}",
                               attributes=(DocumentAttributeVideo(duration=int(data[3]), w=0, h=0),))
        # print('Uploaded')
        # nl = await client.get_entity(bot_link)
        # await client.send_message(bot_link, '/start')
        # await bot.delete_message(data[2], data[4])

        os.unlink(f'videos/{data[2]}.mp4')
        data.clear()

    except ValueError as eee:
        # print(eee)
        pass
    except IndexError as eee:
        # print(eee)
        pass
    except errors.FloodWaitError as e:
        await client.send_message('me', f"Flood wait for {e.seconds}")
    except Exception as ex:
        print(f'{type(ex).__name__}: {ex} | Line: {sys.exc_info()[-1].tb_lineno}')
        pass



if __name__ == '__main__':
    while True:
        client.loop.run_until_complete(send_large_video())
        time.sleep(.1)
