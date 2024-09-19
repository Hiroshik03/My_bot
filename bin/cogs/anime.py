import discord
from discord.commands import slash_command
from discord.ext import commands
import parser_anime
from db_api import anime_db
import UI

class anime(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
    
    @slash_command(name='today_anime', description='Показывает вышедшее сегодня аниме',guild_ids=[1028741714401296444,761259820656754698])
    async def today_anime(self,ctx):
        iteration = 1
        await ctx.respond("Вот список вышедших аниме")
        data = await parser_anime.data_reader()
        embed = discord.Embed(
            title="Anime",
            description=f"Вышедшие сегодня аниме",
            color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
        )
        embed.set_author(name=f"{self.bot.user.display_name}", icon_url=self.bot.user.avatar.url)
        embed.set_image(url=data[iteration][2])
        embed.add_field(name=data[iteration][0],value=data[iteration][1])
        message = await ctx.channel.send(embed=embed)
        while True:
            await message.add_reaction("📄")
            await message.add_reaction("➡")
            await message.add_reaction("✖")
            def check(reaction, user):
                return (user == ctx.author and str(reaction.emoji) == '➡') or (user == ctx.author and str(reaction.emoji) == '📄') or (user == ctx.author and str(reaction.emoji) == '✖')
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except:
                await message.delete()
                return
            match reaction.emoji:
                case "➡" :
                    iteration+=1
                    await message.delete()
                    embed = discord.Embed(
                        title="Anime",
                        description=f"страница №{iteration}",
                        color=discord.Colour.blurple(),  # Pycord provides a class with default colors you can choose from
                    )
                    embed.set_image(url=data[iteration][2])
                    embed.add_field(name=data[iteration][0], value=data[iteration][1])
                    message = await ctx.channel.send(embed=embed)
                case "📄" :
                    await message.delete()
                    await ctx.channel.send ("Больше информации")
                    break
                case "✖":
                    await message.delete()
                    print("Выход")
                    break
    @slash_command(name='search_anime_by_year', description='Поиск аниме по дате выхода', guild_ids=[1028741714401296444,761259820656754698])
    async def search_anime_by_year(self,ctx,type : discord.Option(str,choices=["Year","Name","Genre"]),year):
        if type =="Year":
            iteration = 1
            qeue = 0
            chanel = ctx.channel
            async with anime_db() as db:
                list = await db.search(type = "Year",value = year)
            embed = discord.Embed(
                title="Anime",
                description=f"Топ аниме {year} года",
                color=discord.Colour.blurple(),
            )
            embed.add_field(name=f"**{list[qeue][1]}**", value=f"рейтинг {list[0][3]}🌟",inline=False)
            qeue+=1
            while qeue%10 != 0 and qeue!= len(list)-1:
                qeue+=1
                embed.add_field(name="-----------------------------",value='', inline=False)
                embed.add_field(name=f"**{list[qeue][1]}**", value=f"рейтинг {list[qeue][3]}🌟",inline=False)
            embed.set_author(name=f"{self.bot.user.display_name}", icon_url=self.bot.user.avatar.url)
            await ctx.respond("Поиск...")
            message = await ctx.channel.send(embed=embed)
            while True:
                await message.add_reaction("📄")
                if (qeue!= len(list)-1): await message.add_reaction("➡")
                await message.add_reaction("✖")
                def check(reaction, user):
                    return (user == ctx.author and str(reaction.emoji) == '➡') or (user == ctx.author and str(reaction.emoji) == '📄') or (user == ctx.author and str(reaction.emoji) == '✖')
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except:
                    await message.delete()
                    return
                match reaction.emoji:
                    case "➡" :
                        iteration+=1
                        await message.delete()
                        embed = discord.Embed(
                            title="Anime",
                            description=f"Топ аниме {year} года",
                            color=discord.Colour.blurple(),
                        )
                        embed.set_author(name=f"{self.bot.user.display_name}", icon_url=self.bot.user.avatar.url)
                        qeue += 1
                        embed.add_field(name=f"**{list[qeue][1]}**", value=f"рейтинг {list[qeue][3]}🌟",inline=False)
                        while qeue % 10 != 0 and qeue != len(list)-1:
                            qeue += 1
                            embed.add_field(name="-----------------------------",value='', inline=False)
                            embed.add_field(name=f"**{list[qeue][1]}**", value=f"рейтинг {list[qeue][3]}🌟",inline=False)
                        message = await chanel.send(embed=embed)
                    case "📄" :
                        await message.delete()
                        view = discord.ui.View(timeout=10)
                        view.add_item(UI.anime_selecting(list=list,iteration=iteration))
                        await ctx.send('What is your favourite anime?', view=view)
                        break
                    case "✖":
                        await message.delete()
                        print("Выход")
                        break
        else:
            await ctx.respond("Обновление команды... подождите")

def setup(bot):
    bot.add_cog(anime(bot))