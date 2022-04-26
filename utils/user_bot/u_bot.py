import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon.tl.types import DocumentAttributeVideo
from telethon import TelegramClient
import asyncio
from moviepy.video.io.VideoFileClip import VideoFileClip
from aiogram.bot.api import TelegramAPIServer
from aiogram import Bot, Dispatcher, executor, types
import logging
from database.connection import *

from data import config

local_server = TelegramAPIServer.from_base('http://localhost:8000')
bot = Bot(token=config.BOT_TOKEN, server=local_server, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



async def get_large_video(file_path, user_id, title, msg_id):
    clip = VideoFileClip(file_path)
    dur = int(clip.duration)
    clip.close()

    with db:
        VideosQueue.create(user_id=user_id, title=title, duration=dur, file_path=file_path, post_id=msg_id)

    return



