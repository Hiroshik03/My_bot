import discord
from discord.commands import slash_command
from discord import Option
from datetime import timedelta
from discord.ext import commands
from discord.ext.commands import MissingPermissions
banwords =["ари лох"]
allowed_urls = ["pinterest.com","tenor.com","youtube","spotify","music.yandex.ru","youtu.be"]
role_message_ids =[1285576593997037688]
allowed_guids = [1028741714401296444]
emoji_to_role ={
    "scarlett" :1091833845835366540,
    "__" :1091833845835366540,
}

class moderation(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,message):
        if(not message.author.bot):                         
            print(message.content)
            if(message.content.lower() == "ари расскажи о себе"):
                await message.reply("Я помогаю заблудшими душам этого сервера обрести покой...")
            if(message.content.lower() == "ари сделай чаю" and message.author.id ==357213891513679874):
                await message.reply("Уже бегу!")
            elif (message.content.lower() == "ари сделай чаю" and message.author.id !=357213891513679874):
                await message.reply("Ты не мой хозяин >:с")
            if "https://" in  message.content:
                for url in allowed_urls:
                    if url in message.content:
                        return
                await message.channel.send(f"{message.author.mention}  Ну нельзя тебе такие ссылочки кидать :/")
                await message.delete()
                return
            for word in banwords:
                if(word in message.content.lower()):
                    await message.channel.send(f"{message.author.mention} Сам такой, не ругайся >:c")
                    await message.delete()
    
    @slash_command(name = 'mute', description= 'Выдать мут',guild_ids=[1028741714401296444,761259820656754698])
    @commands.has_permissions(moderate_members=True)
    async def mute (self,ctx, member :Option(discord.Member, required =True), minutes : Option(int, required = True)):
        if member.id == ctx.author.id:
            await ctx.respond("Невозможно замутить самого себя.")
            return
        duration = timedelta(minutes=minutes)
        await member.timeout_for(duration)
        await ctx.respond(f"{member.mention} получил таймаут на {minutes} минут. Посиди подумай над своим поведением >:|")
    @mute.error
    async def muteerror(self,ctx,error):
        if error.original.text =="Missing Permissions":  
            await ctx.respond ("Недостаточно прав для выполнения команды!")
        else:
            await ctx.respond ("Технические шоладки :с")
            raise(error)
            
    @slash_command(name = 'unmute', description= 'Размутить',guild_ids=[1028741714401296444,761259820656754698])
    @commands.has_permissions(moderate_members=True)
    async def unmute (self,ctx, member :Option(discord.Member, required =True), reason :str):
        if member.id == ctx.author.id:
            await ctx.respond("Невозможно размутить самого себя.")
            return
        await member.remove_timeout(reason = reason)
        await ctx.respond(f"{member.mention} мут снят по причине {reason}")
    
    #@slash_command(name = 'role_message', description= 'Создать сообщения для выдачи ролей',guild_ids=[1028741714401296444,761259820656754698])
    #@commands.has_permissions(moderate_members=True)
    #async def role_message(self,ctx,emoji: Option(discord.Emoji,description="выберите emoji",max=5, required = True )):
    #    print(emoji)

    @unmute.error
    async def unmuteerror(self,ctx,error):
        if isinstance(error, MissingPermissions): 
            await ctx.respond ("Недостаточно прав для выполнения команды!")
        else:
            await ctx.respond ("Технические шоладки :с")
            raise(error)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload: discord.RawReactionActionEvent):
        if payload.message_id in role_message_ids:
            role_id = emoji_to_role[payload.emoji.name]
        try:
            guild = self.bot.get_guild(payload.guild_id)
        except:
            print("роли не существует")
        try:
            role = guild.get_role(role_id)    
        except:
            print("Роли не существует")
        try:
            await payload.member.add_roles(role)
        except:
            print("участника не существует")
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload: discord.RawReactionActionEvent):
        if payload.message_id in role_message_ids:
            try:
                guild = self.bot.get_guild(payload.guild_id)
            except:
                pass
            role_id = emoji_to_role[payload.emoji.name]
            
            try:
                role = guild.get_role(role_id)
            except:
                pass 
            try: 
                member = guild.get_member(payload.user_id)   
            except: 
                pass
            await member.remove_roles(role)


            

def setup(bot):
    bot.add_cog(moderation(bot))
