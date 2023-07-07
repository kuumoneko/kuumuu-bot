# from kuumuu_data.config import *

from urllib.request import urlopen
from kuumuu_bot import *

from utility_command.help_command import *
from moderator_command.auto_mod import *
from utility_command.other_command import *
from moderator_command.auto_mod_error import *
import os
from moderator_command.unban import *
from music_command.music_command import*


# --------- Utility Command ---------

@kclient.tree.command(name="news")
async def news(ctx : discord.Interaction):
    embeb = discord.Embed(title='' , color= get_kuumo_color(kuumo_color))
    temp = "`0.1.4`"
    embeb.add_field(name='' , value= f'Kuumuu Client {temp} ' , inline= False)
    embeb.add_field(name='' , value=f'Add some command and Fix some bug')
    await ctx.response.send_message(embed=embeb)

@kclient.tree.command(name="ping" , description="Check client's ping")
async def ping(interaction : discord.Interaction):
    await check_ping(interaction= interaction, ping=int((round(kclient.latency, 10)*1000)))

@kclient.tree.command(name="trans" , description= "Translate like google translate")
async def trans(ctx : discord.Interaction, lang : str, * , string : str ):
    await translate(interaction=ctx, lang=lang  , thing= string)

@kclient.tree.command(name="hello" , description="Say hello to you or other member in your server")
# @app_commands.describe(member = "What would you like to be called?")
async def hello(ctx : discord.Interaction, member: discord.Member = None):
    await hello_member(ctx=ctx, member=member)
    
@kclient.tree.command(name="setnotice" , description="Setup your notifications channel for your server")
@has_permissions(administrator = True)
async def setnotice(ctx : discord.Interaction , room: discord.TextChannel):
    await set_notification(ctx= ctx , room= room)


# ---------- Help Command ----------

@kclient.tree.command(name="help" , description="Auto support from client")
async def help(ctx : discord.Interaction , command_helped : str = None):
    await help_command(ctx= ctx , command_helped= command_helped)

# ---------- Moderator Command ----------

@kclient.tree.command(name="ban", description="Ban a member from your server" )
@has_permissions(ban_members=True)
async def ban(ctx: discord.Interaction, member: discord.Member, *, reason: str =None):
    await ban_member(ctx=ctx, member=member, reason=reason)

@kclient.tree.command(name="unban", description="Unban a member from your server")
@has_permissions(administrator=True)
async def unban(ctx: discord.Interaction):
    await unbanmember(ctx=ctx)

@kclient.tree.command(name="timeout", description="Timeout a member in your server")
@has_permissions(moderate_members = True)
@app_commands.choices(time=[
        app_commands.Choice(name="Second(S)", value="sec"),
        app_commands.Choice(name="Minute(s)", value="min"),
        app_commands.Choice(name="Hour(s)", value="hou"),
        app_commands.Choice(name="Day(s)", value="ds"),
        app_commands.Choice(name="Week(s)", value="we"),
    ])
async def timeout(ctx : discord.Interaction, member: discord.Member, number: int, time: app_commands.Choice[str]):
    await timeout_member(ctx=ctx, member=member, numb=number, string=time)

@kclient.tree.command(name="untimeout", description="Untimeout a member in your server")
@has_permissions(moderate_members = True)
async def untimeout(ctx : discord.Interaction, member: discord.Member):
    await untimeout_member(ctx=ctx, member=member)

@kclient.tree.command(name="kick", description="Kick a member out of your server")
@has_permissions(kick_members=True)
async def kick(ctx : discord.Interaction, member: discord.Member):
    await kick_member(ctx=ctx, member=member)

@kclient.tree.command(name="chnick", description="Change nickname for a member in your server")
async def chnick(ctx: discord.Interaction, member: discord.Member, *, name: str = None):
    await chnick_member(ctx=ctx, member=member, name=name)

@kclient.tree.command(name="chrole", description="Change role for a member in your server")
@has_permissions(manage_roles=True)
async def chrole(ctx: discord.Interaction, member: discord.Member, role: discord.Role):
    await chrole_member(ctx=ctx, member=member, role=role)

# ---------- Moderator Error Command ----------

@timeout.error
async def timeout_error(ctx: discord.Interaction, error):
    await auto_mod_error(ctx=ctx, error=error)

@untimeout.error
async def untimeout_error(ctx: discord.Interaction, error):
    await auto_mod_error(ctx=ctx, error=error)

@chrole.error
async def chrole_error(ctx: discord.Interaction, error):
    await auto_mod_error(ctx=ctx, error=error)

@ban.error
async def ban_error(ctx: discord.Interaction, error):
    await auto_mod_error(ctx=ctx, error=error)

@chnick.error
async def chnick_error(ctx: discord.Interaction, error):
    await auto_mod_error(ctx=ctx, error=error)

@kick.error
async def kick_error(ctx: discord.Interaction, error):
    await auto_mod_error(ctx=ctx, error=error)

# ---------- Chat AI Command ----------

@kclient.tree.command(name="chat", description="Have a chat with ChatGPT")
async def chat(ctx: discord.Interaction, *, message: str):
        if ctx.user == kclient.user:
            return
        username = str(ctx.user)
        kclient.current_channel = ctx.channel
        logger.info(
            f"\x1b[31m{username}\x1b[0m : /chat [{message}] in ({kclient.current_channel})")

        await kclient.enqueue_message(ctx, message)
        
# ---------- Music Command ----------

@kclient.tree.command(name="join" , description="Connect to a voice channel")
async def join(ctx : discord.Interaction):
    await connect(ctx)

@kclient.tree.command(name="leave" , description="Disconnect from a voice channel")
async def leave(ctx : discord.Interaction):
    await disconnect(ctx)
    
@kclient.tree.command(name="play" , description="Play a music")  
async def play(ctx: discord.Interaction):
    await play_music(ctx)
    
@kclient.tree.command(name="aque" , description="Add music to your queue")
async def aque(ctx : discord.Interaction , url: str = None , query:str = None):
    await add_to_queue(ctx , url , query)
    
@kclient.tree.command(name='pause', description='This command pauses the song')
async def pause(ctx: discord.Interaction):
    await pause_music(ctx)
    
@kclient.tree.command(name='resume', description='Resumes the song')
async def resume(ctx: discord.Interaction):
    await resume_music(ctx)
    
@kclient.tree.command(name='stop', description='Stops the song')
async def stop(ctx: discord.Interaction):
    await stop_music(ctx)
    await disconnect(ctx)
        
# ------- Main Bot ---------

@kclient.event
async def on_ready():
    await ready()
    await kclient.send_start_prompt()
    await kclient.tree.sync()
    loop = asyncio.get_event_loop()
    loop.create_task(kclient.process_messages())
    logger.info(f'{kclient.user} is now running!')

@kclient.event
async def on_member_join(member):
    await welcome_member(member=member)

@kclient.event
async def on_member_remove(member):
    await goodbye_member(member=member)

@kclient.event
async def on_message(ctx : discord.Interaction):

    mess = ctx.content
    ten = ctx.author

    if (ten == kclient.user):
        return

    print(mess, " was sent by ", ten)

    if check_tin_juan(mess):
        a = randrange(0, 100, 1)
        if a % 2 == 0:
            await ctx.channel.send(f'tin ko juan e nhé')
        else:
            await ctx.channel.send(f'tin juan lun nhé e')
            
    if mess.startswith(";"):
        temp = (mess.split())
            
        # print(kclient.tree.get_command(temp[0] [1:]) . name)
  

if __name__ == '__main__':    
    # music_command.setup(kclient)
    kclient.run(BOT_TOKEN)