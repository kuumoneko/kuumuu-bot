from urllib.request import urlopen
from kuumuu_bot import *
import os

async def connecting(ctx : discord.Interaction):
    voice_clientt : VoiceClient
    channel = ctx.guild.voice_client.channel
    voice_clientt = discord.utils.get(kclient.voice_clients, guild=ctx.guild)
    if not voice_clientt is None:
        if not voice_clientt.is_connected():
            voice_clientt = await channel.connect()
    else:
        voice_clientt = await channel.connect() 
    return voice_clientt
    

async def playing_music(ctx: discord.Interaction):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    voice_clientt = await connecting(ctx= ctx)
    
    curr_list = music_current_queue[ctx.guild]
    pre_list = music_previous_queue[ctx.guild]
        
    while len(curr_list) != 0:
        
        if(voice_clientt.is_connected() == False):
            return
            
        url = curr_list[0]
        
        song = pafy.new(url=url)  # creates a new pafy object
        audio = song.getbestaudio()  # gets an audio source
        tempp = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
                
        voice_clientt.play(tempp)
        while voice_clientt.is_playing() or voice_clientt.is_paused():
            await asyncio.sleep(0.1)
            
        if len(curr_list) >0 :
            curr_list.popleft()    
            pre_list.append(url)
            if (len(pre_list) > 10):
                pre_list.popleft()
        curr_list = music_current_queue[ctx.guild]        
    return

async def pausing_music(ctx: discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)
    
    if voice_clientt.is_playing():
        voice_clientt.pause()
    
    return

async def resuming_music(ctx: discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)
    
    if voice_clientt.is_paused():
        voice_clientt.resume()
    
    return

async def stopping_music(ctx : discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)
    if (voice_clientt.is_playing()):
        voice_clientt.stop()
    
    return

async def nextting_music(ctx : discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)
    
    if voice_clientt.is_playing():
        voice_clientt.pause()
    
    temp = music_current_queue[ctx.guild][0]
    music_previous_queue[ctx.guild].append(temp)
    music_current_queue[ctx.guild].popleft()
    if voice_clientt.is_paused():
        voice_clientt.resume()
        voice_clientt.stop()
        await playing_music(ctx)
        
    return

async def previousing_music(ctx: discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)
    if voice_clientt.is_playing():
        voice_clientt.pause()
        
    temp = music_previous_queue[ctx.guild][-1]
    music_current_queue[ctx.guild].appendleft(temp)
    music_previous_queue[ctx.guild].pop()
    
    if voice_clientt.is_paused():
        voice_clientt.resume()
        voice_clientt.stop()
        await playing_music(ctx)
        
    return