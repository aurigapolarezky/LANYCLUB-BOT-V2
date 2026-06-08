import discord
from discord import app_commands

def setup_help(bot):

    @bot.command()
    async def help(ctx):

        embed = discord.Embed(
            title="🤖 LANYCLUB BOT",
            description="Daftar command yang tersedia",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="🎸 Community",
            value=
            "`&start`\n"
            "`&faq`\n"
            "`&listevent`\n"
            "`&help`",
            inline=False
        )

        embed.add_field(
            name="📢 Admin Only",
            value=
            "`&event`\n"
            "`&announce`\n"
            "`&deleteevent <id>`",
            inline=False
        )

        await ctx.send(embed=embed)

    @bot.tree.command(
    name="help",
    description="Lihat daftar command"
    )

    async def slash_help(interaction: discord.Interaction
    ):
         await interaction.response.send_message(
        "Gunakan command &announce untuk sementara.\n"
        "Versi slash command sedang dalam pengembangan.",
        ephemeral=True
    )