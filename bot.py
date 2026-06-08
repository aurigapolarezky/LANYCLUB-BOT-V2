from discord.ui import View, Button
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import sqlite3
import asyncio
import random
from data.faq_data import FAQ_DATA
from data.song_database import SONG_DATABASE
import os
from commands.faq import setup_faq
from commands.helpcmd import setup_help
from commands.music import setup_music
from commands.event import setup_event
from commands.announcement import setup_announcement
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

SETUP_CHANNEL_ID = 1464144736943214679
ANNOUNCE_CHANNEL_ID = 1464120119964991589
GENERAL_CHANNEL_ID = 1464121942675296450

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="&", intents=intents, help_command=None)
scheduler = AsyncIOScheduler()

setup_faq(bot)
setup_help(bot)
setup_music(
    bot,
    scheduler,
    GENERAL_CHANNEL_ID
)

setup_event(
    bot,
    scheduler,
    SETUP_CHANNEL_ID,
    ANNOUNCE_CHANNEL_ID,
)

setup_announcement(
    bot,
    SETUP_CHANNEL_ID,
    ANNOUNCE_CHANNEL_ID
)

@bot.event
async def on_ready():
    
    if not scheduler.running:
        scheduler.start()

    synced = await bot.tree.sync()

    print("===== COMMANDS =====")

    for cmd in synced:
        print(cmd.name)

    print("====================")

bot.run(TOKEN)
