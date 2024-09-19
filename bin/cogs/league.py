import discord
import UI
from discord.commands import slash_command
from discord.ext import commands
import League_parse.summoner as search
class league(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @slash_command (name = 'summoner_info', description= 'Поиск призывателей',guild_ids=[1028741714401296444,761259820656754698])
    async def summoner_info(
        self,
        ctx,
        region: discord.Option(str, choices=['ru','euw',"auto"]),
        name :str,
        tag :str = "auto"
        ):
        await ctx.respond("поиск призывателя...")
        try: 
            player = search.summoner_info()
            list = await player.find(region=region,name=name,tag=tag)
            stack =25
            if len(list) > 25:
                for i in range(0, len(list),stack ):
                    view = discord.ui.View(timeout=20)
                    view.add_item(UI.summoner_selecting(player=player,list=list[i:i+stack]))
                    await ctx.send('What is your opinion?', view=view)
            else:   
                view = discord.ui.View(timeout=10)
                view.add_item(UI.summoner_selecting(player=player,list=list))
                await ctx.respond('What is your opinion?', view=view)
            print(1)
        except Exception as err: 
            print (err)
            await ctx.respond("Призыватель не найден :с")
def setup(bot):
    bot.add_cog(league(bot))