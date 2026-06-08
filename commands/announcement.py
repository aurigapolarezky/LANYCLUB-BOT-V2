import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class AnnouncementModal(
    discord.ui.Modal,
    title="Buat Announcement"
):

    def __init__(self, announce_channel_id):
        super().__init__()
        self.announce_channel_id = announce_channel_id

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
        self.announce_channel_id
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

    print("Registering announce slash command")

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
        AnnouncementModal(
            ANNOUNCE_CHANNEL_ID
        )
    )

    @slash_announce.error
    async def announce_error(
    interaction: discord.Interaction,
    error
    ):

        if isinstance(
        error,
        app_commands.MissingPermissions
        ):

            await interaction.response.send_message(
            "❌ Hanya administrator yang dapat menggunakan command ini.",
            ephemeral=True
            )