import discord

from discord.ext import commands

class Chat_tools(commands.Cog):

    ''' Chat tools class '''

    def __init__(self, bot):

        self.bot = bot

    @commands.command(pass_context = True, name = 'clear', help = 'Elimina mensajes del chat, puedes especificar cuantos')
    async def clear(self, ctx, amount=1):

        ''' Delete n amount of messages '''

        await ctx.channel.purge(limit=amount+1)
        await ctx.channel.send(f'Se borraron {amount} mensajes')


    @commands.command(pass_context = True, name = 'ping', help = 'Indica la latencia')
    async def ping(self, ctx):

        ''' Measure latency '''

        latency = self.bot.latency
        await ctx.channel.send(f"Latencia: {round(latency*1000)}ms")


def setup(bot):

    ''' Chat setup '''

    bot.add_cog(Chat_tools(bot))