import discord
from datetime import datetime , timedelta
from discord.ext import commands
from discord.commands import slash_command
from discord.ext import tasks
from contextlib import AsyncContextDecorator
from db_api import stats_db

import asyncio

class statistics(commands.Cog,AsyncContextDecorator):
    now_online = []
    def __init__(self,bot):
        self.bot = bot
    
    @slash_command(name = 'member_stats', description= 'Просмотреть статистику пользователся на сервере',guild_ids=[1028741714401296444,761259820656754698])
    async def member_stats(self,ctx, member : discord.Option(discord.Member,required =True)):
        async with stats_db() as db:
            stats = await db.get_stats(member.id,ctx.guild.id)
            time = timedelta(seconds=0)
            for stat in stats:
                join = datetime.strptime(stat[0], "%Y-%m-%d %H:%M:%S")
                leave = datetime.strptime(stat[1], "%Y-%m-%d %H:%M:%S")
                time += leave-join
            await ctx.respond(f"Пользователь {member.nick} общался на протяжении : {time}")
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if not before.channel:
            print(f"user {member.nick} join on time {datetime.now().replace(microsecond=0)}")
            async with stats_db() as db:
                await db.on_join(member.guild,after.channel,member)
        if not after.channel:
            print(f"user {member.nick} leave on time {datetime.now().replace(microsecond=0)}")
            async with stats_db() as db:
                await db.on_leave(member)
        else:
            return       
def setup(bot):
    bot.add_cog(statistics(bot))

    
    
    
    
    