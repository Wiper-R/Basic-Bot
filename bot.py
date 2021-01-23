from discord.ext import commands
import discord
import config

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print("Bot is Ready!")


for ext in ('example', 'database', 'levelling'):
    bot.load_extension(f'cogs.{ext}')

bot.mongo = bot.get_cog('Database')
bot.run(config.TOKEN)
