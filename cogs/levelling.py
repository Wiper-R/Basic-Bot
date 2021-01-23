import discord
from discord.ext import commands
import random


class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def calculate_xp(self, level: int):
        return (1 + level) * (20 + level)

    @commands.Cog.listener('on_message')
    async def message_handler(self, message: discord.Message):
        if message.guild is None:
            return

        if message.author.bot:
            return

        increased_xp = random.randint(10, 25)
        user = await self.bot.mongo.fetch_member(message.author)
        next_level_xp = self.calculate_xp(user.level + 1)
        user.xp += increased_xp

        if user.xp > next_level_xp:
            user.xp = 0
            user.level += 1

        update = user.to_mongo(update=True)
        if update is not None:
            await self.bot.mongo.db.member.update_one({'guild_id': message.guild.id, 'member_id': message.author.id}, update)

        if update is not None and "level" in update['$set']:
            await message.channel.send(f'Congratulations, {message.author.mention} you level upped to {user.level:,}.')

    @commands.command()
    async def rank(self, ctx: commands.Context):
        user = await self.bot.mongo.fetch_member(ctx.author)
        embed = discord.Embed(title='Your Rank!')
        embed.add_field(name='Level', value=f'{user.level:,}')
        embed.add_field(
            name='Xp', value=f'{user.xp:,}/{self.calculate_xp(user.level + 1)}')
        embed.color = discord.Color.red()
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Levelling(bot))
