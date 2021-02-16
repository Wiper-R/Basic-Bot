from discord.ext import commands
import config
import discord


intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print("Bot is Ready!")


for ext in ('fun', 'levelling'):
    bot.load_extension(f'cogs.{ext}')

bot.run(config.TOKEN)
