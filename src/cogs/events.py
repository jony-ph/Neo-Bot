import discord

from discord.ext import commands

class Events(commands.Cog):

    ''' Class of all events  '''

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        print("Bot en línea")

def setup(bot):

    ''' Events setup '''

    bot.add_cog(Events(bot))