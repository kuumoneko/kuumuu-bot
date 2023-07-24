from kuumuu_bot import *
from main_bot.support import *

async def check_ping(interaction : discord.Interaction , ping: int):
    embed=discord.Embed(title="", description="", color=get_kuumo_color(kuumo_color)) 
    embed.add_field(name="", value=f'Pong! Now, Ping of kuumuu is { int((round(kclient.latency, 10)*1000)) } ms', inline=False)
    await interaction.response.send_message(embed=embed)
    
async def translate(interaction : discord.Interaction , lang , thing: str):
    
    translator = Translator()
    translation = translator.translate(thing, dest=lang)
    embeb = discord.Embed(title='' , color= get_kuumo_color(kuumo_color))
    embeb.add_field(name='' , value=f'{translation.text}')
    await interaction.response.send_message(embed= embeb)
    
async def hello_member(ctx : discord.Interaction , member:discord.Member = None):
    time = datetime.now
    hou = time().hour
    kuumo = "hello"
    kuumoid = emoji[kuumo]
    print(kuumoid)
    
    embeb = discord.Embed(title='' , color= get_kuumo_color(kuumo_color))
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
    
async def set_notification(ctx :discord.Interaction , room: discord.TextChannel):
    kuumo = open("notification.txt" , "w")
    
    temp = str(ctx.guild.id)
    kurru[temp] = room.id
    
    for it in kclient.guilds:
        temp = str(it.id)
        # print("             " , it.id , ' ' , kurru[temp])
        
        if kurru[temp] == "Not Present":
            continue
        tempp = str(temp) + " " + str(kurru[temp]) + chr(13)
        kuumo.write(tempp)
        
    channel = kclient.get_channel(room.id)
    embeb = discord.Embed(title="" , color= get_kuumo_color(kuumo_color))
    embeb.add_field(name = '' , value= f'<#{room.id}> has been set into the Announcement Room')
    await ctx.response.send_message(embed= embeb)
    
async def ready():
    # language()
    get_color()
    keep_alive()
    get_emoji(kclient)
    # print(emoji["hello"])
    get_notifi()
    print('We have logged in as {0.user}'.format(kclient))

async def welcome_member(member : discord.Member):
    
    temp = member.guild.id
    
    # print(temp, ' ' ,kurru[str(temp)])
    channel = kclient.get_channel(int(kurru[str(temp)])) # replace with your channel ID
    role = discord.utils.get(member.guild.roles, name="member") # replace with your role name
    await member.add_roles(role)
    embeb = discord.Embed(title="" , color= get_kuumo_color(kuumo_color))
    embeb.add_field(name ='' ,value= f"Welcome to the server, {member.mention}! You have been given the {role} role.")
    await channel.send(embed= embeb)
    
async def goodbye_member(member : discord.Member):
    temp = member.guild.id
    
    # print(temp, ' ' ,kurru[str(temp)])
    channel = kclient.get_channel(int(kurru[str(temp)])) # replace with your channel ID
    embeb = discord.Embed(title="" , color= get_kuumo_color(kuumo_color))
    embeb.add_field(name = '' , value= f"Goodbye, {member.mention}! We'll miss you.")
    await member.send(embed= embeb)
    await channel.send(embed= embeb)