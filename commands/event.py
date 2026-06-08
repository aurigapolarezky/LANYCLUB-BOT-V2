import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import sqlite3
from discord import app_commands

conn = sqlite3.connect("events.db")
cursor = conn.cursor()

def setup_event(
    bot,
    scheduler,
    SETUP_CHANNEL_ID,
    ANNOUNCE_CHANNEL_ID
):

    @bot.command()
    async def listevent(ctx):
        rows = cursor.execute(
            "SELECT * FROM events"
        ).fetchall()

        if not rows:
            await ctx.send("Tidak ada event aktif.")
            return

        text = "**Event Aktif**\n\n"

        for row in rows:
            text += (
                f"ID: {row[0]}\n"
                f"Judul: {row[1]}\n"
                f"Tanggal: {row[2]}\n"
                f"Jam: {row[3]}\n\n"
            )

        await ctx.send(text)

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def deleteevent(ctx, event_id: int):

        cursor.execute(
            "DELETE FROM events WHERE id=?",
            (event_id,)
        )
        conn.commit()

        await ctx.send(
            f"🗑️ Event {event_id} dihapus."
        )

    @bot.tree.command(
    name="event",
    description="Membuat event baru"
    )

    @bot.tree.command(
    name="deleteevent",
    description="Menghapus event"
    )

    @bot.tree.command(
    name="listevent",
    description="Menampilkan event aktif"
    )

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def event(ctx):

        if ctx.channel.id != SETUP_CHANNEL_ID:
            await ctx.send(
                "❌ Command ini hanya bisa digunakan di channel setup."
            )
            return

        def check(m):
            return (
                m.author == ctx.author and
                m.channel == ctx.channel
            )

        questions = [
            "📌 Judul event?",
            "📅 Tanggal? (YYYY-MM-DD)",
            "🕒 Jam? (HH:MM)",
            "📍 Tempat?",
            "📝 Deskripsi?",
            "👥 Mention? (`everyone` atau nama role)"
        ]

        answers = []

        try:
            for q in questions:
                await ctx.send(q)
                msg = await bot.wait_for(
                    "message",
                    check=check,
                    timeout=300
                )
                answers.append(msg.content)

        except asyncio.TimeoutError:
            await ctx.send("❌ Waktu pengisian habis.")
            return
        judul, tanggal, jam, tempat, deskripsi, mention_input = answers

        try:
            datetime.strptime(f"{tanggal} {jam}", "%Y-%m-%d %H:%M")
        except ValueError:
                await ctx.send("❌ Format tanggal/jam salah.")
                return

        role = None

        if mention_input.lower() == "everyone":
           mention_text = "@everyone"
        else:
            role = discord.utils.find(
        lambda r: r.name.lower() == mention_input.lower(),
        ctx.guild.roles
        )

        if role is None:

           role_list = "\n".join(
            [f"• {r.name}" for r in ctx.guild.roles if not r.is_default()]
           )

        await ctx.send(
            f"❌ Role tidak ditemukan.\n\n"
            f"Role yang tersedia:\n{role_list}"
        )
        return

        mention_text = role.mention

        cursor.execute(
        """
        INSERT INTO events
        (judul,tanggal,jam,tempat,deskripsi,mention)
        VALUES(?,?,?,?,?,?)
        """,
        (judul, tanggal, jam, tempat, deskripsi, mention_text)
        )
        conn.commit()

        event_id = cursor.lastrowid

        schedule_event(
        event_id, judul, tanggal, jam,
        tempat, deskripsi, mention_text
        )

        await ctx.send(f"✅ Event '{judul}' berhasil dibuat. ID: {event_id}")

