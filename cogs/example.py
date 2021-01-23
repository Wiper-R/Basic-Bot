import discord
from discord.ext import commands


# @bot.command() > @commands.command()
# @bot.event > @commands.Cog.listener()

def setup(bot: commands.Bot):
    bot.add_cog(Example(bot))


class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot is Ready, in example cog.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(message.author)
