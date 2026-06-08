import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class AnnouncementModal(
    discord.ui.Modal,
    title="Buat Announcement"
):

    judul = discord.ui.TextInput(
        label="Judul Announcement",
        placeholder="Contoh: Jadwal Nobar"
    )

    isi = discord.ui.TextInput(
        label="Isi Announcement",
        style=discord.TextStyle.paragraph
    )

    mention = discord.ui.TextInput(
        label="Mention",
        placeholder="everyone / none / nama role"
    )

    banner = discord.ui.TextInput(
        label="Gunakan Banner?",
        placeholder="yes / no"
    )

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        channel = interaction.client.get_channel(
            ANNOUNCE_CHANNEL_ID
        )

        if channel is None:

            await interaction.response.send_message(
                "❌ Channel announce tidak ditemukan.",
                ephemeral=True
            )
            return

        mention_text = ""

        if self.mention.value.lower() == "everyone":

            mention_text = "@everyone"

        elif self.mention.value.lower() != "none":

            role = discord.utils.find(
                lambda r:
                r.name.lower() ==
                self.mention.value.lower(),
                interaction.guild.roles
            )

            if role:
                mention_text = role.mention

        embed = discord.Embed(
            title=f"📢 {self.judul}",
            description=self.isi,
            color=discord.Color.green()
        )

        if self.banner.value.lower() == "yes":

            try:

                file = discord.File(
                    "banner.png",
                    filename="banner.png"
                )

                embed.set_image(
                    url="attachment://banner.png"
                )

                await channel.send(
                    content=mention_text,
                    embed=embed,
                    file=file
                )

            except FileNotFoundError:

                await interaction.response.send_message(
                    "❌ banner.png tidak ditemukan.",
                    ephemeral=True
                )

                return

        else:

            await channel.send(
                content=mention_text,
                embed=embed
            )

        await interaction.response.send_message(
            "✅ Announcement berhasil dikirim.",
            ephemeral=True
        )
def setup_announcement(
    bot,
    SETUP_CHANNEL_ID,
    ANNOUNCE_CHANNEL_ID
):

 @bot.command()
 @commands.has_permissions(administrator=True)
 async def announce(ctx):

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

    try:

        await ctx.send("📢 Judul announcement?")
        judul = (
            await bot.wait_for(
                "message",
                check=check,
                timeout=300
            )
        ).content

        await ctx.send("📝 Isi announcement?")
        isi = (
            await bot.wait_for(
                "message",
                check=check,
                timeout=300
            )
        ).content

        roles_text = "\n".join(
            [
                f"• {r.name}"
                for r in ctx.guild.roles
                if not r.is_default()
            ]
        )

        await ctx.send(
            "👥 Mention siapa?\n\n"
            "Ketik:\n"
            "`everyone`\n"
            "`none`\n"
            "atau nama role\n\n"
            f"{roles_text}"
        )

        mention_input = (
            await bot.wait_for(
                "message",
                check=check,
                timeout=300
            )
        ).content

        await ctx.send(
            "🖼️ Gunakan banner?\n\n"
            "yes / no"
        )

        banner_choice = (
            await bot.wait_for(
                "message",
                check=check,
                timeout=300
            )
        ).content.lower()

    except asyncio.TimeoutError:

        await ctx.send(
            "❌ Waktu pengisian habis."
        )
        return

    # ==========================
    # MENTION
    # ==========================

    if mention_input.lower() == "everyone":

        mention_text = "@everyone"

    elif mention_input.lower() == "none":

        mention_text = ""

    else:

        role = discord.utils.find(
            lambda r:
            r.name.lower() ==
            mention_input.lower(),
            ctx.guild.roles
        )

        if role is None:

            await ctx.send(
                "❌ Role tidak ditemukan."
            )
            return

        mention_text = role.mention

    # ==========================
    # EMBED
    # ==========================

    embed = discord.Embed(
        title=f"📢 {judul}",
        description=isi,
        color=discord.Color.green()
    )

    channel = bot.get_channel(
        ANNOUNCE_CHANNEL_ID
    )

    if channel is None:

        await ctx.send(
            "❌ Channel announce tidak ditemukan."
        )
        return

    # ==========================
    # DENGAN BANNER
    # ==========================

    if banner_choice == "yes":

        try:

            file = discord.File(
                "banner.png",
                filename="banner.png"
            )

            embed.set_image(
                url="attachment://banner.png"
            )

            await channel.send(
                content=mention_text,
                embed=embed,
                file=file
            )

        except FileNotFoundError:

            await ctx.send(
                "❌ banner.png tidak ditemukan."
            )
            return

    # ==========================
    # TANPA BANNER
    # ==========================

    else:

        await channel.send(
            content=mention_text,
            embed=embed
        )

    await ctx.send(
        "✅ Announcement berhasil dikirim."
    )

    @bot.tree.command(
    name="announce",
    description="Membuat announcement"
    )

    @app_commands.checks.has_permissions(
    administrator=True
    )
    
    async def slash_announce(
    interaction: discord.Interaction
    ):

        await interaction.response.send_modal(
        AnnouncementModal()
        )