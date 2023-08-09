from kuumuu_import import *
# from src.aclient import aclient
class Ulitlity():
    def __init__(self , client ) -> None:
        self.__client__ = client
        super().__init__()
        
    async def news(self, ctx : discord.Interaction ):
        embeb = discord.Embed(title='' , color= self.__client__.support.get_kuumo_color())
        temp = "`0.8.2`"
        embeb.add_field(name=f'Kuumuu Client {temp} ' , 
                        value=f'`Fix some small bug` \n `Add Auto update requirements`')
        await ctx.response.send_message(embed=embeb)
    
    async def ping(self , interaction : discord.Interaction , ping: int):
        embed=discord.Embed(title="", description="", color= self.__client__.support.get_kuumo_color()) 
        embed.add_field(name="", value=f'Pong! Now, Ping of kuumuu is { int((round(self.__client__.latency, 10)*1000)) } ms', inline=False)
        await interaction.response.send_message(embed=embed)
        
    async def trans(self , interaction : discord.Interaction , lang , thing: str):
        await interaction.response.defer(thinking=True)
        translation = Translator().translate(text=thing, dest=lang , src='auto')
        embeb = discord.Embed(title='' , color= self.__client__.support.get_kuumo_color()) 
        embeb.add_field(name='' , value=f'{translation.text}')
        await interaction.followup.send(embed= embeb)
        
    async def hello(self , ctx : discord.Interaction , member:discord.Member = None):
        time = datetime.datetime.now()
        hou = time.hour
        kuumo = "hello"
        kuumoid = self.__client__.support.emojii[kuumo]
        
        embeb = discord.Embed(title='' , color= self.__client__.support.get_kuumo_color()) 
        temp: str
        if member == None:
            if hou >= 5 and hou <= 10:
                temp = (f"chào buổi sáng {ctx.user.mention} , buổi sáng tốt lành <:{kuumo}:{kuumoid}>")
            elif hou >= 11 and hou <= 13:
                temp = (f"chào buổi trưa {ctx.user.mention} , buổi trưa tốt lành <:{kuumo}:{kuumoid}>")
            elif hou >= 14 and hou <= 17:
                temp = (f"chào buổi chiều {ctx.user.mention} , buổi chiều tốt lành <:{kuumo}:{kuumoid}>")
            elif hou >= 17 and hou <= 21:
                temp = (f"chào buổi tối {ctx.user.mention} , buổi tối tốt lành <:{kuumo}:{kuumoid}>")
            else:
                kuumo = "sleep"
                kuumoid = emoji[kuumo]
                temp = (f"Khuya rồi mà {ctx.user.mention} , thoi kệ chúc ngủ ngon tui ngủ đây <:{kuumo}:{kuumoid}>")
                
        else:
            if hou >= 5 and hou <= 10:
                temp = (f"chào buổi sáng {member.mention} , buổi sáng tốt lành <:{kuumo}:{kuumoid}>")    
            elif hou >= 11 and hou <= 13:
                temp = (f"chào buổi trưa {member.mention} , buổi trưa tốt lành <:{kuumo}:{kuumoid}>")
            elif hou >= 14 and hou <= 17:
                temp = (f"chào buổi chiều {member.mention} , buổi chiều tốt lành <:{kuumo}:{kuumoid}>")
            elif hou >= 17 and hou <= 21:
                temp =(f"chào buổi tối {member.mention} , buổi tối tốt lành <:{kuumo}:{kuumoid}>")
            else:
                kuumo = "sleep"
                kuumoid = emoji[kuumo]
                temp = (f"Khuya rồi mà {member.mention} , thoi kệ chúc ngủ ngon <@{ctx.user.id}> ngủ đây <:{kuumo}:{kuumoid}>")
        
        embeb.add_field(name='' , value= temp)
        
        await ctx.response.send_message(embed= embeb)
        
    async def setnotice(self , ctx :discord.Interaction , room: discord.TextChannel):
        kuumo = open("kuumuu_data\\notification.txt" , "w")
        
        temp = str(ctx.guild.id)
        self.__client__.support.notification[temp] = str(room.id)
        
        for it in self.__client__.guilds:
            temp = str(it.id)
            # print("             " , it.id , ' ' , kurru[temp])
            
            if self.__client__.support.notification[temp] == "Not Present":
                continue
            
            tempp = str(temp) + " " + str(self.__client__.support.notification[temp]) + chr(13)
            kuumo.write(tempp)
            
        channel = self.__client__.get_channel(room.id)
        embeb = discord.Embed(title="" , color= self.__client__.support.get_kuumo_color()) 
        embeb.add_field(name = '' , value= f'<#{room.id}> has been set into the Announcement Room')
        await ctx.response.send_message(embed= embeb)
        
