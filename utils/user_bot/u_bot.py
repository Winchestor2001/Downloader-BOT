import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon.tl.types import DocumentAttributeVideo
from telethon import TelegramClient
import asyncio
from moviepy.video.io.VideoFileClip import VideoFileClip
from aiogram import Bot, Dispatcher, executor, types
import logging
from database.connection import *

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



async def get_large_video(file_path, user_id, title, msg_id):
    clip = VideoFileClip(file_path)
    dur = int(clip.duration)
    clip.close()

    with db:
        VideosQueue.get_or_create(user_id=user_id, title=title, duration=dur, file_path=file_path, post_id=msg_id)

    return



