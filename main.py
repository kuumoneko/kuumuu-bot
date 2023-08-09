import inspect
from urllib.request import urlopen
from kuumuu_import import *
from kuumuu_bot import kclient

# --------- Utility Command ---------

# @kclien(name="news" , description="News about this bot")
@kclient.tree.command(name="news" , description="News about this bot")
async def news(ctx: discord.Interaction):
    await kclient.ulti.news(ctx= ctx)
    
@kclient.tree.command(name="test" , description="tesing")
@is_owner()
async def test(ctx: discord.Interaction):
    return

@kclient.tree.command(name="ping" , description="Check client's ping")
async def ping(ctx : discord.Interaction):
    await kclient.ulti.ping(interaction= ctx, ping=int((round(kclient.latency, 10)*1000)))

@kclient.tree.command(name="trans" , description= "Translate like google translate")
@app_commands.describe(lang= str("mói"))
@app_commands.describe(string=str("lmao"))
async def trans(ctx : discord.Interaction, 
                lang : str ,
                string : str
                ):
    await kclient.ulti.trans(interaction=ctx, lang=lang  , thing= string)

@kclient.tree.command(name="hello" , description="Say hello to you or other member in your server")
@app_commands.describe(member = "Who would you like to be called?")
async def hello(ctx : discord.Interaction, member: discord.Member = None):
    await kclient.ulti.hello(ctx=ctx, member=member)
    
@kclient.tree.command(name="setnotice" , description="Setup your notifications about member enter and leave your server channel for your server")
@has_permissions(administrator = True)
@app_commands.describe(room= "What room would you like to be called?")
async def setnotice(ctx : discord.Interaction , room: discord.TextChannel):
    await kclient.ulti.setnotice(ctx= ctx , room= room)

# ---------- Help Command ----------

@kclient.tree.command(name="help" , description="Auto support from client")
@app_commands.describe(command_helped= "Command that you need help")
async def help(ctx : discord.Interaction , command_helped : str = None):
    await kclient.help.help(ctx= ctx , command= command_helped)

# ---------- Moderator Command ----------

@kclient.tree.command(name="ban", description="Ban a member from your server" )
@has_permissions(ban_members=True)
@app_commands.describe(member = "Who would you like to be called?")
@app_commands.describe(reason = "Why would you do that?")
async def ban(ctx: discord.Interaction, member: discord.Member, *, reason: str =None):
    await kclient.mod.ban(ctx=ctx, member=member, reason=reason)

@kclient.tree.command(name="bans", description="Unban a member from your server")
@has_permissions(administrator=True)
async def bans(ctx: discord.Interaction): 
    await kclient.mod.bans(ctx=ctx )

@kclient.tree.command(name="timeout", description="Timeout a member in your server")
@has_permissions(moderate_members = True)
@app_commands.choices(time=[
        app_commands.Choice(name="Second(S)", value="sec"),
        app_commands.Choice(name="Minute(s)", value="min"),
        app_commands.Choice(name="Hour(s)", value="hou"),
        app_commands.Choice(name="Day(s)", value="ds"),
        app_commands.Choice(name="Week(s)", value="we"),
    ])
@app_commands.describe(member = "Who would you like to be called?")
@app_commands.describe(number = "How long would you like to be used?")
@app_commands.describe(time = "What would you like to be used?")
async def timeout(ctx : discord.Interaction, member: discord.Member, number: int, time: app_commands.Choice[str]):
    await kclient.mod.timeout(ctx=ctx, member=member, numb=number, string=time)

@kclient.tree.command(name="untimeout", description="Untimeout a member in your server")
@has_permissions(moderate_members = True)
@app_commands.describe(member = "Whoe would you like to be called?")
async def untimeout(ctx : discord.Interaction, member: discord.Member):
    await kclient.mod.untimeout(ctx=ctx, member=member)

@kclient.tree.command(name="kick", description="Kick a member out of your server")
@has_permissions(kick_members=True)
@app_commands.describe(member = "Who would you like to be called?")
async def kick(ctx : discord.Interaction, member: discord.Member):
    await kclient.mod.kick(ctx=ctx, member=member)

@kclient.tree.command(name="chnick", description="Change nickname for a member in your server")
@app_commands.describe(member = "Who would you like to be called?")
@app_commands.describe(name = "What name would you like to change?")
async def chnick(ctx: discord.Interaction, member: discord.Member, *, name: str = None):
    await kclient.mod.chnick(ctx=ctx, member=member, name=name)

@kclient.tree.command(name="chrole", description="Change role for a member in your server")
@has_permissions(manage_roles=True)
@app_commands.describe(member = "Who would you like to be called?")
@app_commands.describe(role = "What role would you like to be called?")
async def chrole(ctx: discord.Interaction, member: discord.Member, role: discord.Role):
    await kclient.mod.chrole(ctx=ctx, member=member, role=role)

@kclient.tree.command(name="warn" , description="Warn a member")
@has_permissions(moderate_members = True)
@app_commands.describe(member= "Who would you like to be called?")
@app_commands.describe(reason= "Why would you do that?")
async def warn(ctx : discord.Interaction , member : discord.Member , reason : str):
    await kclient.mod.warn(ctx , member , reason)

# ---------- Chat AI Command ----------

@kclient.tree.command(name="chat", description="Have a chat with ChatGPT")
@app_commands.choices(isprivate=[
                app_commands.Choice(name="True" , value= "True"),
                app_commands.Choice(name= "False" , value= "False")
])
@app_commands.choices(chatbot=[
                        app_commands.Choice(name="Bing AI Creative" , value="Bing Creative"),
                        app_commands.Choice(name="Bing AI Balanced" , value="Bing Balanced"),
                        app_commands.Choice(name="Bing AI Precise" , value="Bing Precise"),
                        app_commands.Choice(name="Google Bard" , value="Bard")
])
@app_commands.describe(message = "What do you want to ask Kuumuu?")
@app_commands.describe(isprivate = "Do you want to ask private?")
@app_commands.describe(chatbot = "What chat bot you want to use?")
async def chat(ctx: discord.Interaction, message:str , isprivate : app_commands.Choice[str]  , chatbot: app_commands.Choice[str]):
    await kclient.ai.chat(ctx , message , isprivate.value , chatbot.value)
        
# ---------- Music Command ----------

@kclient.tree.command(name="join" , description="Connect to a voice channel")
async def join(ctx : discord.Interaction):
    await kclient.music.join(ctx)

@kclient.tree.command(name="leave" , description="Disconnect from a voice channel")
async def leave(ctx : discord.Interaction):
    await kclient.music.leave(ctx)
    
@kclient.tree.command(name='pause', description='This command pauses the song')
async def pause(ctx: discord.Interaction):
    await kclient.music.pause(ctx)
    
@kclient.tree.command(name='resume', description='Resumes the song')
async def resume(ctx: discord.Interaction):
    await kclient.music.resume(ctx)
    
@kclient.tree.command(name='stop', description='Stops the song')
async def stop(ctx: discord.Interaction):
    await kclient.music.stop(ctx= ctx , id = ctx.guild_id)
    await kclient.music.leave(ctx= ctx)
    
@kclient.tree.command(name="ntrack" , description="Play next track in queue")
async def ntrack(ctx: discord.Interaction):
    await kclient.music.ntrack(ctx= ctx , id=ctx.guild_id)

@kclient.tree.command(name="ptrack" , description="Play previous track in queue")
async def ptrack(ctx: discord.Interaction):
    await kclient.music.ptrack(ctx=ctx , id= ctx.guild_id)
    
@kclient.tree.command(name="play" , description="Play a track")  
@app_commands.choices(isloop=[
        app_commands.Choice(name="True", value="True"),
        app_commands.Choice(name="False", value="False")
    ])
@app_commands.choices(shuffle=[
        app_commands.Choice(name="The next queue", value="1" ),
        app_commands.Choice(name="All track" ,value="2" ),
    ])
@app_commands.describe(prompt= "Link Youtube or query to Search on Youtube")
@app_commands.describe(isloop = "Do you want your track is repeated?")
@app_commands.describe(shuffle = "What mode would be used?")
async def play(ctx: discord.Interaction,
                prompt : str = "None",
                isloop : app_commands.Choice[str] = "None", 
                shuffle: app_commands.Choice[str] = "None"
            ):
    await ctx.response.defer(thinking=True)
    
    if ctx.user.voice.channel == None:
        ctx.followup.send(f"There is nothing to play :<")
        return
    
    list = None
    url = None
    query = None

    if prompt.find('playlist?list=') != -1:
        list = prompt
    elif prompt.find('watch?=') != -1 or prompt.find('youtu.be/') != -1:
        url = prompt
    elif prompt != "None":
        query = prompt
    
    if (url != None or query != None or list != None):
        kclient.music.__isdone__ = False
        await kclient.music.__add_to_queue__(ctx , url , query , list)
        
        while(kclient.music.__isdone__ == False):
            await asyncio.sleep(0.00000001)
    
    if type(isloop) != str and isloop.value == "True":
        kclient.music.__isloop__[ctx.guild_id] = True
    elif type(isloop) != str and isloop.value == "False":
        kclient.music.__isloop__[ctx.guild_id] = False
        
    if type(shuffle) != str:
        if shuffle.value == "1":
            await kclient.music.shuffle(ctx= ctx , id= ctx.guild_id , mode = "True")
            return
        elif shuffle.value == "2":
            await kclient.music.shuffle(ctx= ctx , id= ctx.guild_id , mode= "False")
            return
        
    await kclient.music.play(ctx= ctx , id= ctx.guild_id)
    
@kclient.tree.command(name="setloop" , description="Set repeating for your music")
@app_commands.choices(loop=[
        app_commands.Choice(name="True", value="True"),
        app_commands.Choice(name="False", value="False")
    ])
@app_commands.describe(loop = "Do you want your track is repeated?")
async def setloop(ctx : discord.Interaction , loop : app_commands.Choice[str]):
    await kclient.music.setloop(ctx , loop)

@kclient.tree.command(name="shuffle" , description="Shuffle your track")
@app_commands.choices(mode=[
        app_commands.Choice(name="The next queue", value="True" ),
        app_commands.Choice(name="All track" ,value="False" )
    ])
@app_commands.describe(mode = "What mode would be used")
async def shuffle(ctx : discord.Interaction , mode : app_commands.Choice[str]):
    await kclient.music.shuffle(ctx= ctx , id= ctx.guild_id , mode= mode)
    
@kclient.tree.command(name="queue" ,description="Show the queue")
async def queue(ctx: discord.Interaction):
    await kclient.music.queue(ctx= ctx , id=ctx.guild_id)
    
@kclient.tree.command(name="nplay" , description="Show the current playing track")
async def nplay(ctx : discord.Interaction):
    
    await kclient.music.nplay(ctx= ctx, id= ctx.guild_id)


# ------- Main Bot ---------

@kclient.event
async def on_ready():
    
    kclient.support.get_notifi()
    kclient.support.get_emoji()
    await kclient.tree.sync()
    loop = asyncio.get_event_loop() 
    loop.create_task(kclient.support.update_database())
    loop.create_task(kclient.ai.__chatting__.process_messages())
    logger.info(f'{kclient.user} is now running!')

@kclient.event
async def on_member_join(member):
    temp = member.guild.id 
    
    role = discord.utils.get(member.guild.roles, name="member") # replace with your role name
    await member.add_roles(role)
    
    if kclient.support.notification[str(temp)] == None:
        return
        
        
       
    channel = kclient.get_channel(int( kclient.support.notification[str(temp)]) ) # replace with your channel ID
    
    embeb = discord.Embed(title="" , color= kclient.support.get_kuumo_color())
    embeb.add_field(name ='' ,value= f"Welcome to the server, {member.mention}! You have been given the {role} role.")
    await channel.send(embed= embeb)

@kclient.event
async def on_member_remove(member : discord.Member):
    temp = member.guild.id
    
    if kclient.support.notification[str(temp)] == None:
        return
    
    channel = kclient.get_channel(int( kclient.support.notification[str(temp)]) ) # replace with your channel ID
    embeb = discord.Embed(title="" , color= kclient.support.get_kuumo_color())
    embeb.add_field(name = '' , value= f"Goodbye, {member.mention}! We'll miss you.")
    await channel.send(embed= embeb)
    await member.send(embed=embeb)

@kclient.event
async def on_voice_state_update( member, before, after):
    
    if member.id == kclient.user.id:
        return
    
    if after.channel != before.channel and after.channel == None :
        # voice = 
        voice = get(kclient.voice_clients, guild=member.guild)
        cnt = 0
        
        if voice == None:
            return
        
        while len(before.channel.members) < 2:
            cnt = cnt + 0.1
            await asyncio.sleep(0.1)
            if (cnt > 3.5):
                await voice.disconnect()

@kclient.tree.error
async def on_app_command_error(ctx: discord.Interaction, error):
    try:
        await ctx.response.send_message(f"Something was wrong.\nError:\n ```{error}```\nPlease call my owner for helping!")
        
    except:
        
        try: 
            await ctx.followup.send(f"Something was wrong.\nError:\n ```{error}```\nPlease call my owner for helping!")
        
        except:
                
            try:
                await ctx.edit_original_response(f"Something was wrong.\nError:\n ```{error}```\nPlease call my owner for helping!")
                
            except:
                await ctx.channel.send(f"Something was wrong.\nError:\n ```{error}```\nPlease call my owner for helping!")
    raise error

@kclient.event
async def on_message(ctx : discord.Message):

    mess = ctx.content
    ten = ctx.author

    if (ten == kclient.user):
        return
    
    if len(ctx.attachments) > 0:
        attachment = ctx.attachments[0]
    
        if attachment.filename.endswith(".jpg") or attachment.filename.endswith(".jpeg") or attachment.filename.endswith(".png") or attachment.filename.endswith(".webp") or attachment.filename.endswith(".gif"):
            image = attachment.url
            print(f"{image} {mess}  was sent by {ten}")
        elif "https://images-ext-1.discordapp.net" in ctx.content or "https://tenor.com/view/" in mess:

            print(f"{mess} " , " was sent by ", ten)
    else:
        print(mess, " was sent by ", ten)

    if kclient.support.check_tin_juan(a= mess):
        a = randrange(0, 100, 1)
        if a % 2 == 0:
            await ctx.channel.send(f'tin ko juan e nhé')
        else:
            await ctx.channel.send(f'tin juan lun nhé e')
            
    mention = kclient.user.id
    ment = f"Hey <@{mention}>"
    if ment in mess:
        print(mess[len(ment) : ])
            
    if kclient.user.mentioned_in(ctx):
        await ctx.channel.send('You mentioned me!')
            
if __name__ == '__main__':
    update.update()
    
    kclient.run(kclient.TOKEN)