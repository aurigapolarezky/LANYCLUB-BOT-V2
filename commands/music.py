def setup_music(
    bot,
    scheduler,
    GENERAL_CHANNEL_ID
):
    
 async def send_daily_mood_poll():

    global last_poll_message_id

    channel = bot.get_channel(
        GENERAL_CHANNEL_ID
    )

    if channel is None:
        return

    poll = await channel.send(
        "@everyone\n\n"
        "💙 Haii LANY Fam!\n\n"
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

    scheduler.add_job(
    send_daily_mood_poll,
    "cron",
    hour=17,
    minute=00
    )

    scheduler.add_job(
    send_song_of_the_day,
    "cron",
    hour=19,
    minute=00
    )

    async def send_song_of_the_day():

        global last_poll_message_id

        if last_poll_message_id is None:
            return

        channel = bot.get_channel(
            GENERAL_CHANNEL_ID
        )

        if channel is None:
            return

        try:

            poll_msg = await channel.fetch_message(
                last_poll_message_id
            )

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

        result = {
            "senang": happy,
            "sedih": sad,
            "biasa": normal
        }

        mood = max(
            result,
            key=result.get
        )

        song = random.choice(
            SONG_DATABASE[mood]
        )

        mood_icon = {
            "senang": "😊",
            "sedih": "😔",
            "biasa": "😐"
        }

        embed = discord.Embed(
            title="🎵 Song of the Day",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Mood Hari Ini",
            value=f"{mood_icon[mood]} {mood.title()}",
            inline=False
        )

        embed.add_field(
            name="Lagu",
            value=song["title"],
            inline=False
        )

        embed.add_field(
            name="Album",
            value=song["album"],
            inline=False
        )

        embed.set_footer(
            text="Semoga lagu ini menemani malam kalian @everyone\n\n💙"
        )

        file = discord.File(
            song["banner"],
            filename="album.jpg"
        )
        
        embed.set_image(
            url="attachment://album.jpg"
        )

        await channel.send(
            "@everyone",
            embed=embed,
            file=file
        )