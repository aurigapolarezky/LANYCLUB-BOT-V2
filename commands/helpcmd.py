import discord

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