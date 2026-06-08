import discord
from discord.ui import View, Button
from discord.ext import commands
from data.faq_data import FAQ_DATA
from data.song_database import SONG_DATABASE
from discord import app_commands

def create_faq_embed(category):

    embed = discord.Embed(
        title=f"📚 {category}",
        description="Pilih pertanyaan yang ingin dilihat.",
        color=discord.Color.blue()
    )

    return embed

class FAQCategoryView(View):

    def __init__(self):
        super().__init__(timeout=120)

        categories = list(FAQ_DATA.keys())

        icons = [
            "🎸",
            "💿",
            "🌹",
            "🌙",
            "🧸",
            "🏙️",
            "💙",
            "🐑",
            "🎵",
            "✨"
        ]

        for i, category in enumerate(categories):

            button = Button(
                label=category,
                emoji=icons[i],
                style=discord.ButtonStyle.primary
            )

            async def callback(interaction, cat=category):
                await interaction.response.send_message(
                    embed=create_faq_embed(cat),
                    view=FAQQuestionView(cat),
                    ephemeral=True
                )

            button.callback = callback
            self.add_item(button)

class FAQQuestionView(View):

    def __init__(self, category):
        super().__init__(timeout=120)

        questions = list(
            FAQ_DATA[category].keys()
        )

        for question in questions:

            button = Button(
                label=question[:80],
                style=discord.ButtonStyle.secondary
            )

            async def callback(
                interaction,
                q=question,
                cat=category
            ):

                await interaction.response.send_message(
                    FAQ_DATA[cat][q],
                    ephemeral=True
                )

            button.callback = callback
            self.add_item(button)


def setup_faq(bot):

    @bot.command()
    async def faq(ctx):

        embed = discord.Embed(
            title="📚 LANY FAQ CENTER",
            description=(
                "Selamat datang di **LANY FAQ Center**! 🌹\n\n"
                "Tempat terbaik untuk mencari tahu segala hal tentang LANY, mulai dari General, album, lagu, hingga fakta menarik lainnya.\n\n"
                "**Silakan pilih kategori di bawah ini untuk melihat detailnya!** ✨"
            ),
            color=discord.Color.blue()
        )

        await ctx.send(
            embed=embed,
            view=FAQCategoryView()
        )

    @bot.command()
    async def start(ctx):

        embed = discord.Embed(
            title="🎸 Halo!",
            description=
            f"Haiii {ctx.author.mention}! 👋\n\n"
            "Aku **LANYCLUB BOT** 🤖✨\n\n"
            "Aku siap membantu menjawab pertanyaan "
            "tentang LANY, album, lagu, "
            "dan berbagai hal lainnya.",
            color=discord.Color.purple()
        )

        await ctx.send(embed=embed)

    @bot.tree.command(
    name="faq",
    description="Buka LANY FAQ Center"
    )

    @bot.tree.command(
    name="start",
    description="Memulai penggunaan bot"
    )

    async def slash_faq(interaction: discord.Interaction
    ):
         await interaction.response.send_message(
        "Gunakan command &announce untuk sementara.\n"
        "Versi slash command sedang dalam pengembangan.",
        ephemeral=True
    )