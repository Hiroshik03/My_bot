import json
import discord
import cloudscraper
from discord.ext import commands
from discord.commands import slash_command
cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
with open("secrets.json") as f:
    data = json.load(f)
    usa_proxy = data["proxy"]["USA"]


class SearchErr(Exception):
    def __init__(self, *args):
        if args:
            self.message =args[0]
        else:
            self.message = "Ошибка поиска нет постов с таким тегом"
    def __str__ (self):
        return self.message


class rule34(commands.Cog):
    def __init__(self,bot):
        self.search_link = "https://r34.app/posts/rule34.xxx?tags="
        self.alt_search_link = "https://alt2.r34.app/posts/rule34.xxx?tags="
        self.pos = []
        self.bot = bot
    async def find(self,my_str,search,last = 0):
        if my_str.find(search) != -1:
            res = my_str.find(search)
            self.pos.append(res+last)
            await self.find(my_str[res+3:],search,res+last+3)
        else :
            if not self.pos:
                raise SearchErr
            return
    async def search(self,tags =[], video = False):
        res =[]
        if video:
            tags.append('animated')
        if len(tags) == 1:
            scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
            link = self.search_link
            link +=tags[0] 
            retry = 0
            while True:
                retry+=1
                print(f"Попытка номер {retry}")
                try:
                    response1 = scraper.get(link, proxies=usa_proxy, cookies=cookies,verify=False).text
                except:
                    continue
                break
            if video:
                await self.find(response1,".mp4")
                await self.find(response1,".gif")
            for i in self.pos:
                    res.append(response1[:i+4][i-79 + response1[:i+4][i-79:].find("https"):])      
            else:
                await self.find(response1,".jpg")
                await self.find(response1,".jpeg")
                await self.find(response1,".png")
                #int(response1[:i][i-130:][response1[:i][i-130:].find('t":')+3:][:response1[:i][i-130:].find('t":')-1])
                for i in self.pos:
                    if (response1[:i][i-130:].find("video") == -1) and (response1[:i][i-130:].find("img") != -1) and (int(response1[:i][i-130:][response1[:i][i-130:].find('height="')+8:].split('"')[0])> 35):
                        res.append(response1[:i+4][i-100 + response1[:i+4][i-100:].find("https"):])
                    else:
                        continue
        else:
            link = self.search_link
            link+=tags[0]
            for tag in tags[1:]:
                link +=f"%7C{tag}"
            scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
            retry = 0
            while True:
                retry+=1
                print(f"Попытка номер {retry}")
                try:
                    response1 = scraper.get(link, proxies=usa_proxy, cookies=cookies).text
                except:
                    continue
                break
            if video:
                await self.find(response1,".mp4")
                for i in self.pos:
                    res.append(response1[:i+4][i-79 + response1[:i+4][i-79:].find("https"):])
            else:
                await self.find(response1,".jpg")
                for i in self.pos:
                    if response1[:i][i-130:].find("video") == -1:
                        res.append(response1[:i+4][i-100 + response1[:i+4][i-100:].find("https"):])
                    else:
                        continue
        return res
    @slash_command(name = 'rule34', description= 'Интересный контент (Тэги добавляются через пробел)',guild_ids=[1028741714401296444,761259820656754698,1283828596636385362])
    async def rule34(self,ctx, tags,video : bool = False, max : int= 1):
        self.pos = []
        await ctx.respond("Поиск контента...")
        tags = tags.lower().split(' ')
        try:
            result = await self.search(tags,video)
        except Exception as err:
            await ctx.channel.send(err)
        for url in result[:max]:
            await ctx.channel.send(url)
            
def setup(bot):
     bot.add_cog(rule34(bot))






#find(string,"mp4")
#print(pos)
#print(string[80])