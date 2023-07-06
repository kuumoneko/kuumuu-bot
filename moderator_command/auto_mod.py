from kuumuu_bot import *
from main_bot.support import *
from moderator_command.unban import *
from moderator_command.auto_mod_error import *

# ---------- Auto Mod Command ----------

async def ban_member(ctx : discord.Interaction, member: discord.Member , reason = None):
    if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
        embeb = discord.Embed(title='' , color= get_kuumo_color(kuumo_color))
        
        messageok = f"{member} đã bị ban bởi {ctx.user.name} với lý do {reason}"
        
        embeb.add_field(name='' , value= messageok)
        await member.send(embed= embeb)
        await ctx.response.send_message(embed=embeb)
        await member.ban(reason=reason)
    else:
        raise MissingPermissions()
    
async def unbanmember(ctx: discord.Interaction):
    await unban_member(ctx=ctx)
    
async def timeout_member(ctx :discord.Interaction , member:discord.Member , numb:int , string : app_commands.Choice[str]):
    if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
        embed=discord.Embed(title="", description="", color=get_kuumo_color(kuumo_color)) 
        time = string.value
        print(time)
        chara = time
        # print("                  " , chara)
        val = ""
        if chara == "sec" or chara == "min" or chara == "hou" or chara == "ds" or chara == "we":
            val = f'{member.name} has been bonked by {ctx.user.name} in {numb} {timee[chara]}'
        elif (chara[ : -1] == 's'):
            val = f'{member.name} has been bonked by {ctx.user.name} in {numb} {chara}'
        elif chara.startswith('second') or chara.startswith('minute') or chara.startswith('hour') or chara.startswith('day') or chara.startswith('week'):
            val = f'{member.name} has been bonked by {ctx.user.name} in {numb} {chara}s'
        else:
            await auto_mod_error(ctx= ctx , error= "InvalidArgument")
            return
            
        embed.add_field(name="", value=val, inline=False)
        await ctx.response.send_message(embed=embed)
        if chara == "sec" or chara.startswith('second') :
            await member.timeout( timedelta(seconds= numb))
        elif chara == "min" or chara.startswith('minute'):
            await member.timeout(timedelta(minutes= numb) ) 
        elif chara == "hou" or chara.startswith('hour'):
            await member.timeout( timedelta(hours= numb) ) 
        elif chara == "ds" or chara.startswith('day'):
            await member.timeout( timedelta(days= numb) ) 
        elif chara == "we" or chara.startswith('week'):
            await member.timeout( timedelta(weeks= numb) ) 

    else:
        raise MissingPermissions()
        
async def untimeout_member(ctx : discord.Interaction, member: discord.Member):
    if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
        emmeb = discord.Embed(title='' , color= get_kuumo_color(kuumo_color))
        emmeb.add_field(name='' , value=f'{member} has been untimeout by {ctx.user}')
        await ctx.response.send_message(embed=emmeb)
        await member.untimeout()
    else:
        raise MissingPermissions()

async def kick_member(ctx : discord.Interaction, member: discord.Member  ):
    
    if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
        await member.kick()
        emmeb = discord.Embed(title='' , color= get_kuumo_color(kuumo_color))
        emmeb.add_field(name='' , value=f'{member} has been kicked by {ctx.user}')
        await ctx.response.send_message(embed= emmeb)
    else:
        raise MissingPermissions()

async def chnick_member(ctx : discord.Interaction, member: discord.Member , name : str):
    if (member == ctx.user and ctx.permissions.manage_nicknames):
        await member.edit(nick= name)
        await ctx.response.send_message(f'Done' , ephemeral= True)
    elif ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role and ctx.permissions.manage_nicknames:
        await member.edit(nick= name)
        await ctx.response.send_message(f'Done' , ephemeral= True)
    else:
        raise MissingPermissions()
    
async def chrole_member(ctx: discord.Interaction, member:discord.Member , role: discord.Role):
    if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.response.send_message(f'Done' , ephemeral= True)
        else:
            await member.add_roles(role)
            await ctx.response.send_message(f'Done' , ephemeral= True)
    else:
        raise MissingPermissions()
