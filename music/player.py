import asyncio
import discord

from music.state import get_player
from music.ytdl import FFMPEG_OPTIONS


async def play_next(bot, guild):

    player = get_player(guild.id)

    # Jika queue kosong
    if len(player["queue"]) == 0:
        player["current"] = None
        return

    # Ambil lagu pertama
    song = player["queue"].pop(0)
    player["current"] = song

    voice = guild.voice_client

    if voice is None:
        return

    source = discord.FFmpegOpusAudio(
        song["url"],
        **FFMPEG_OPTIONS
    )

    def after_play(error):
        if error:
            print(error)

        future = asyncio.run_coroutine_threadsafe(
            play_next(bot, guild),
            bot.loop
        )

        try:
            future.result()
        except Exception as e:
            print(e)

    voice.play(
        source,
        after=after_play
    )