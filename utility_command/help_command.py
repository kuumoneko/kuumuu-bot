from kuumuu_bot import *


async def help_command(ctx : discord.Interaction , command_helped : str = None):
    help_embeb = discord.Embed(title='', color=get_kuumo_color(kuumo_color))

    # setup user's avatar
    tempp: discord.Member
    tempp = ctx.user
    ava = str(tempp.avatar)
    url = ava[: -10]
    help_embeb.set_thumbnail(url=f'{url}')
    
    # for slash_command in kclient.tree.walk_commands():
    #     print(slash_command)
    
    mod_temp = ["ban" , "unban" , "timeout" , "untimeout" , "kick" , "chnick" , "chrole"]
    uti_temp = ["ping" , "setnotice" , "news" , "trans" , "hello"]
    AI_temp  = ["chat"]
    music_temp = ["join" , "leave" , "play" , "pause" , "resume" , "stop" , "ntrack" , "ptrack"]
    

    if command_helped == None:
        
        # setup sth before helping
        help_embeb.add_field(name=f'Help Command Menu ',
                             value=f'I am here to help you, {ctx.user.mention}!', 
                             inline=False)

        help_embeb.add_field(name='', 
                             value=f'Call `/command` to use command {chr(13)}For more info on a specific command, use `/help command`',
                             inline= False)

        #  Auto Mod Command Help
        kuumo = ""
        
        for i in mod_temp:
            temp = f'{i}'
            temp = "`" + temp + "`"
            kuumo = kuumo + f" {temp} "
        help_embeb.add_field(name=f'Moderation:', value=kuumo, inline=False)

        # Utility Command Help
        
        kuumo = ""
        for i in uti_temp:
            temp = f'{i}'
            temp = "`" + temp + "`"
            kuumo = kuumo + f" {temp} "
        help_embeb.add_field(name=f'Utility:', value=kuumo, inline=False)

        # AI command Help
        
        kuumo = ""
        for i in AI_temp:
            temp = f'{i}'
            temp = "`" + temp + "`"
            kuumo = kuumo + f" {temp} "
        help_embeb.add_field(name=f'AI support:', value=kuumo, inline=False)
        
        kuumo = ""
        for i in music_temp:
            temp = f'{i}'
            temp = "`" + temp + "`"
            kuumo = kuumo + f" {temp} "
        help_embeb.add_field(name=f'Music:' , value=kuumo , inline=False)
        

        await ctx.response.send_message(embed=help_embeb)
    else:
        kurumo = kclient.tree.get_command(command_helped)
        
        help_embeb.add_field(name=f'Overview:',
                             value=f'Name: {kurumo.name} {chr(13)}Description: {kurumo.description}',
                             inline= False
                             )
        
        moi :str
        if kurumo.name in mod_temp:
            moi = kurumo.name + " member"
        else:
            moi = "no"
            
        help_embeb.add_field(name="Main:",
                             value=f'How to call: `/{kurumo.name}` {chr(13)}You need {moi} permission(s) to use that command',
                             inline= False
                             )
        
        moi = ""
        for i in kurumo.parameters:
            moi = moi + i.name
            if (i.name == "member"):
                moi = moi + ": Your server's member"
            elif i.name == "number":
                moi = moi + ": A number :)))"
            elif i.name == "reason":
                moi = moi + ": Reason why you do that activity"
            elif i.name == "time":
                moi = moi + ": An unit of measurement of time"
            elif i.name == "name":
                moi = moi + ": A name"
            elif i.name == "room":
                moi = moi + ": A channel of your server"
            elif i.name == "string":
                moi = moi + ": A string"
            elif i.name == "lang":
                moi = moi + ": A language"
            elif i.name == "url":
                moi = moi + ": A Youtube Url"
            elif i.name == "query":
                moi = moi + ": A name you want to search on Youtube"
            
            moi = moi + chr(13)
            
        if (len(moi) < 1):
            moi = "None"
        
        help_embeb.add_field(name="Arguments:",
                             value=f'{moi}',
                             inline= False
                             
                             )
        
        await ctx.response.send_message(embed= help_embeb)
        pass