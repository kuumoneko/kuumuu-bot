from urllib.request import urlopen
from kuumuu_bot import *
import os

async def play_music(ctx: discord.Interaction , lists : Queue):
    
    if not ctx.user.voice.channel in ctx.guild.voice_channels:
        await ctx.user.voice.channel.connect()
    
    while len(lists) != 0:
        temp = lists.get()
        ctx.guild.voice_client.play(temp)
        
        voice_clientt = VoiceClient(ctx.guild.voice_client)
        while voice_clientt.is_playing():
            asyncio.sleep(0.1)
        

        
        
        
    
    
    
    return