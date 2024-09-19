import random
import discord
from discord.commands import slash_command
from discord.ext import commands

class fun(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    @slash_command(name='roll', description='Роллит случайное число',guild_ids=[1028741714401296444,761259820656754698])
    async def roll(self,ctx ,at:int = 0,to:int =100):
        generate = random.randrange(start=at, stop=to)
        embed = discord.Embed(
            title="Rolled",
            description=f":slot_machine: {generate}",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )
        embed.set_author(name=f"{ctx.user.display_name}", icon_url=ctx.user.avatar.url)
        await ctx.respond(embed=embed)
    @slash_command(name='meme', description='Мемчик',guild_ids=[1028741714401296444,761259820656754698])
    async def meme(self,ctx):
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()
        voice_client.create
        audio_source = discord.FFmpegPCMAudio('test.mp3')
        voice_client.play(audio_source)
        
def setup(bot):
    bot.add_cog(fun(bot))