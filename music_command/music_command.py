
from urllib.request import urlopen
from kuumuu_bot import *
import os
from music_command.music_playing import *


async def connect(ctx : discord.Interaction):
    channel = ctx.user.voice.channel
    # ensure there is a player_manager when creating a new voice_client
    await channel.connect()
    await ctx.response.send_message(f'{kclient.user.name} has been connected to <#{channel.id}>')


async def disconnect(ctx : discord.Interaction):
    channel = ctx.guild.voice_client
    # print(channel.channel)
    await channel.disconnect()
    await ctx.response.send_message(f'{kclient.user.name} has been disconnected from <#{channel.id}>')    
    

async def play_music(ctx: discord.Interaction):
    embeb = discord.Embed(title="" , color=get_kuumo_color(kuumo_color))
    if ctx.user.voice.channel == None:
        embeb.add_field(name=f'"No Voice Channel' , value=f'You need to be in a voice channel to use this command!')
        await ctx.response.send_message(embed=embeb)
        return
    
    voicechannel = ctx.user.voice.channel
    channel_bot = kclient.voice_clients
    temp = []

    for voice_client in channel_bot:
        voice_channel = voice_client.channel
        temp.append(voice_channel)
    if not voicechannel in temp:
        await voicechannel.connect()
        
    await playing_music(ctx=ctx)
    
async def add_to_queue(ctx: discord.Interaction , url: str = None , query: str = None):
    
    embeb = discord.Embed(title="" , color=get_kuumo_color(kuumo_color))
    
    if query != None:
        search = query.replace(" ", "+")
        search = "https://www.youtube.com/results?search_query=" + search
        html = urlopen(search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        await ctx.response.send_message("https://www.youtube.com/watch?v=" + video_ids[0])
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        
        music_queue[ctx.user].put(url)
        print(music_queue[ctx.user].qsize())
        return
        
    elif url != None:
        await ctx.response.send_message(url)    
        music_queue[ctx.user].put(url)
        print(music_queue[ctx.user].qsize())
        return
    else:
        embeb.add_field(name="Warning:" , value=f'Please use youtube_url or query to search on youtube!')
        await ctx.response.send_message(embed= embeb)
        return
    
    
async def pause_music(ctx: discord.Interaction):
    await pausing_music(ctx)
    
async def resume_music(ctx: discord.Interaction):
    await resuming_music(ctx)        
        
async def stop_music(ctx: discord.Interaction):
    await stopping_music(ctx)