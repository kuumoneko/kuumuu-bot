from urllib.request import urlopen
from kuumuu_bot import *
import os

async def playing_music(ctx: discord.Interaction):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    voice_clientt : VoiceClient
    channel = ctx.guild.voice_client.channel
    voice_clientt = discord.utils.get(kclient.voice_clients, guild=ctx.guild)
    if not voice_clientt is None:
        if not voice_clientt.is_connected():
            voice_clientt = await channel.connect()
    else:
        voice_clientt = await channel.connect() 
    lists = music_queue[ctx.user]
        
    while lists.qsize() != 0:
        
        if(voice_clientt.is_connected() == False):
            print("lmao")
            return
            
        url = lists.get()
        print(lists.qsize())
        song = pafy.new(url=url)  # creates a new pafy object
        audio = song.getbestaudio()  # gets an audio source
        tempp = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
                
        voice_clientt.play(tempp)
        while voice_clientt.is_playing() or voice_clientt.is_paused():
            await asyncio.sleep(0.1)
            
        lists = music_queue[ctx.user]        
    return

async def pausing_music(ctx: discord.Interaction):
    voice_clientt : VoiceClient
    channel = ctx.guild.voice_client.channel
    voice_clientt = discord.utils.get(kclient.voice_clients, guild=ctx.guild)
    if not voice_clientt is None:
        if not voice_clientt.is_connected():
            voice_clientt = await channel.connect()
    else:
        voice_clientt = await channel.connect() 

    print("voice_clientt ", voice_clientt.is_playing() , " playing")
    
    if voice_clientt.is_playing():
        voice_clientt.pause()
    
    return

async def resuming_music(ctx: discord.Interaction):
    voice_clientt : VoiceClient
    channel = ctx.guild.voice_client.channel
    voice_clientt = discord.utils.get(kclient.voice_clients, guild=ctx.guild)
    if not voice_clientt is None:
        if not voice_clientt.is_connected():
            voice_clientt = await channel.connect()
    else:
        voice_clientt = await channel.connect() 
        
    print("voice_clientt ", voice_clientt.is_paused() , " paused")
    
    if voice_clientt.is_paused():
        voice_clientt.resume()
    
    return

async def stopping_music(ctx : discord.Interaction):
    voice_clientt : VoiceClient
    channel = ctx.guild.voice_client.channel
    voice_clientt = discord.utils.get(kclient.voice_clients, guild=ctx.guild)
    if not voice_clientt is None:
        if not voice_clientt.is_connected():
            voice_clientt = await channel.connect()
    else:
        voice_clientt = await channel.connect() 
        
    print("voice_clientt ", voice_clientt.is_paused() , " paused")
    if (voice_clientt.is_playing()):
        voice_clientt.stop()
    
    return