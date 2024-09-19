import discord
from discord.commands import slash_command
from discord.ext import commands

class test(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @slash_command(guild_ids = [1028741714401296444] ,name="ping", description ="Показывает задержку бота")
    async def ping (self,ctx):
        await ctx.respond(self.bot.latency)

def setup(bot):
    bot.add_cog(test(bot))