import discord
from db_api import anime_db
import parsetest
import League_parse.summoner as summoner
class anime_selecting(discord.ui.Select):
    def __init__(self, list,iteration):
        options =[]
        for i in range(iteration*10):
            options.append(discord.SelectOption(label=list[i][1], description='Your favourite anime', emoji='🟦'))
        super().__init__(placeholder='Pick your colour', min_values=1, max_values=1, options=options)
    async def callback(self,interaction):
        async with anime_db() as db:
            anime = await db.search("Name",self.values[0])
        more_info = await parsetest.more_info(anime[0][4])
        embed = discord.Embed(
        title=f"{anime[0][1]}",
        description=f"",
        color=discord.Colour.blurple(),
        )
        #embed.set_author(name=f"{bot.user.display_name}", icon_url=bot.user.avatar.url)
        embed.set_image(url=anime[0][2])
        embed.add_field(name="Жанр:",value=anime[0][6])
        embed.add_field(name="Рейтинг",value=anime[0][3])
        if more_info[0][3]=="None":
            embed.add_field(name="Серии", value=more_info[0][1])
        else:
            embed.add_field(name="Серии", value=more_info[0][1])
            embed.add_field(name="Статус",value=more_info[0][3])
        embed.add_field(name="Описание",value=more_info[0][2])
        await interaction.response.send_message(embed=embed)
        await interaction.channel.send(f'{more_info[0][0]}')
class summoner_selecting (discord.ui.Select):
    def __init__(self, list,player):
        options =[]
        self.list = list
        self.player = player
        for i in list:
            options.append(discord.SelectOption(label=i.nick, description='Your choice', emoji='🟦'))
        super().__init__(placeholder='Pick your opinion', min_values=1, max_values=1, options=options)
    async def callback(self,interaction):
        for i in self.list:
            if i.nick == self.values[0]:
                self.player = i
                break
        await summoner.summoner_info.fill(self.player)
        embed = discord.Embed(
        title=self.player.nick,
        description=f"",
        color=discord.Colour.blurple(),
        )
        embed.set_thumbnail(url=self.player.icon_url)
        embed.add_field(name="Уровень", value = self.player.level)
        embed.add_field(name="Ранг", value = f"{self.player.rank}\n")
        embed.add_field(name="Игры", value = self.player.win_lose)
        embed.add_field(name="Винрейт", value =self.player.winrate)
        embed.set_image(url=self.player.rank_icon)
        await interaction.response.send_message(embed=embed)
        await interaction.message.delete()
    async def on_timeout(self):
        print("test")