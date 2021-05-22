import discord
import os

from discord.ext import commands

bot = commands.Bot(command_prefix='/')
COGS_FOLDER = './src/cogs'

# Load the cogs
for filename in os.listdir(COGS_FOLDER):

    if filename.endswith('.py'):

        bot.load_extension(f'cogs.{filename[:-3]}')

# Bot's token
bot.run(os.environ[DISCORD_BOT_TOKEN]) 