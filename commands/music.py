import random
import discord
from data.song_database import SONG_DATABASE
from music.state import get_player
from music.ytdl import ytdl, FFMPEG_OPTIONS
from discord import app_commands
import yt_dlp
from music.ytdl import (
    get_song_info,
    FFMPEG_OPTIONS
)
from music.state import get_player

last_poll_message_id = None

def setup_music(bot, scheduler, GENERAL_CHANNEL_ID):

    async def send_daily_mood_poll():
        global last_poll_message_id

        channel = bot.get_channel(GENERAL_CHANNEL_ID)
        if channel is None:
            return

        poll = await channel.send(
            "@everyone\n\n"
            "💙 Haiii guyys!\n\n"
            "Bagaimana kabar kalian hari ini?\n\n"
            "Semoga harimu menyenangkan ya ✨\n\n"
            "Aku ingin menyiapkan Song of the Day "
            "berdasarkan mood kalian hari ini 🎵\n\n"
            "😊 = Senang\n"
            "😔 = Sedih\n"
            "😐 = Biasa Saja\n\n"
            "Pilih salah satu yaa~\n"
            "Jam 19:00 aku akan mengumumkan hasilnya 💙"
        )

        await poll.add_reaction("😊")
        await poll.add_reaction("😔")
        await poll.add_reaction("😐")

        last_poll_message_id = poll.id

    async def send_song_of_the_day():
        global last_poll_message_id

        if last_poll_message_id is None:
            return

        channel = bot.get_channel(GENERAL_CHANNEL_ID)
        if channel is None:
            return

        try:
            poll_msg = await channel.fetch_message(last_poll_message_id)
        except:
            return

        happy = 0
        sad = 0
        normal = 0

        for reaction in poll_msg.reactions:
            if str(reaction.emoji) == "😊":
                happy = reaction.count - 1
            elif str(reaction.emoji) == "😔":
                sad = reaction.count - 1
            elif str(reaction.emoji) == "😐":
                normal = reaction.count - 1

        result = {"senang": happy, "sedih": sad, "biasa": normal}

        mood = max(result, key=result.get)

        song = random.choice(SONG_DATABASE[mood])

        mood_icon = {"senang": "😊", "sedih": "😔", "biasa": "😐"}

        embed = discord.Embed(
            title="🎵 Song of the Day", color=discord.Color.blue()
        )

        embed.add_field(
            name="Mood Hari Ini",
            value=f"{mood_icon[mood]} {mood.title()}",
            inline=False,
        )
        embed.add_field(name="Lagu", value=song["title"], inline=False)
        embed.add_field(name="Album", value=song["album"], inline=False)

        embed.set_footer(text="Semoga lagu ini menemani malam kalian 💙")

        file = discord.File(song["banner"], filename="album.jpg")
        embed.set_image(url="attachment://album.jpg")

        await channel.send("@everyone", embed=embed, file=file)

    scheduler.add_job(
        send_daily_mood_poll,
        "cron",
        hour=10,
        minute=0,
        id="daily_poll",
        replace_existing=True,  
    )

    scheduler.add_job(
        send_song_of_the_day,
        "cron",
        hour=12,
        minute=0,
        id="daily_song",
        replace_existing=True,
    )

    @bot.tree.command(
    name="join",
    description="Bot bergabung ke voice channel"
    )
    async def slash_join(
        interaction: discord.Interaction
    ):

        if interaction.user.voice is None:
            await interaction.response.send_message(
            "❌ Kamu harus berada di voice channel.",
            ephemeral=True
            )
            return

        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is None:
            await channel.connect()
        else:
            await interaction.guild.voice_client.move_to(channel)

        await interaction.response.send_message(
            f"🎵 Berhasil bergabung ke **{channel.name}**."
        )

    @bot.tree.command(
    name="stop",
    description="Menghentikan musik dan keluar dari voice channel"
    )
    async def slash_stop(
        interaction: discord.Interaction
    ):

        voice = interaction.guild.voice_client

        if voice is None:
            await interaction.response.send_message(
                "❌ Bot sedang tidak berada di voice channel.",
                ephemeral=True
            )
            return

        player = get_player(interaction.guild.id)
        player["queue"].clear()
        player["current"] = None

        await voice.disconnect()

        await interaction.response.send_message(
            "⏹️ Music player dihentikan dan bot keluar dari voice channel."
        )

    @bot.tree.command(
    name="play",
    description="Memutar lagu dari YouTube"
    )
    async def slash_play(
        interaction: discord.Interaction,
        lagu: str
    ):

        if interaction.user.voice is None:
            await interaction.response.send_message(
                "❌ Kamu harus berada di voice channel.",
                ephemeral=True
            )
            return

        await interaction.response.defer()

        voice = interaction.guild.voice_client

        if voice is None:
            channel = interaction.user.voice.channel
            voice = await channel.connect()

        player = get_player(
            interaction.guild.id
        )

        song = await get_song_info(lagu)

        player["queue"].append(song)

        await interaction.followup.send(
            f"🎵 **{song['title']}** ditambahkan ke queue!"
        )

    print("Music scheduler loaded")
    print(scheduler.get_jobs())