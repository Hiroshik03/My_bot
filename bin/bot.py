import discord
import json
cogs = ["cogs.anime","cogs.fun","cogs.league","cogs.moderation","cogs.rule34","cogs.statistics","cogs.test"]
bot = discord.Bot()

with open("secrets.json") as f:
    data = json.load(f)
    API_KEY = data["bot"]["API_KEY"]

@bot.event
async def on_ready():
    print(f"{bot.user.display_name} Готов!")
for cog in cogs:
    bot.load_extension(cog)
    print (f"расширение {cog} загружено!")
bot.run(API_KEY)