
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
    
    
async def pause_music(ctx: discord.Interaction):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.response.send_message("The bot is not playing anything at the moment.")
    
    pass


async def play_music(ctx: discord.Interaction, url:str = None , query : str = None):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        
    embeb = discord.Embed(title="" , color=get_kuumo_color(kuumo_color))
    if ctx.user.voice.channel == None:
        embeb.add_field(name=f'"No Voice Channel' , value=f'You need to be in a voice channel to use this command!')
        await ctx.response.send_message(embed=embeb)
        return

    channel = ctx.user.voice.channel
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice_client = discord.utils.get(kclient.client.voice_clients, guild=ctx.guild)
    
    if voice_client == None:
        await voice.connect()
    else:
        await voice_client.move_to(channel)
        
    if query != None:
        search = query.replace(" ", "+")
        search = "https://www.youtube.com/results?search_query=" + search
        html = urlopen(search)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        await ctx.response.send_message("https://www.youtube.com/watch?v=" + video_ids[0])
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        
        song = pafy.new(url=url)  # creates a new pafy object
        audio = song.getbestaudio()  # gets an audio source
        temp = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
        
        if not channel in ctx.guild.voice_channels:
            await channel.connect()
        music_queue[ctx.user].append(temp)
        # ctx.guild.voice_client.play(temp)
        return
        
    elif url != None:
        
        channel = ctx.user.voice.channel

        song = pafy.new(url=url)  # creates a new pafy object
        audio = song.getbestaudio()  # gets an audio source
        temp = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
        
        if not channel in ctx.guild.voice_channels:
            await channel.connect()
            
        music_queue[ctx.user].put(temp)
        # ctx.guild.voice_client.play(temp)
        await ctx.response.send_message(url)
        return
    
    elif len(music_queue[ctx.user]) != 0:
        
        return
        
    else:
        embeb.add_field(name="Warning:" , value=f'Please use youtube_url or query to search on youtube!')
        await ctx.response.send_message(embed= embeb)
        return
    
    
async def pause_music(ctx: discord.Interaction):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.response.send_message("The bot is not playing anything at the moment.")
    
async def resume_music(ctx: discord.Interaction):
    voice_client = ctx.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.response.send_message("The bot was not playing anything before this. Use play_song command")
        
        
async def stop_music(ctx: discord.Interaction):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.response.send_message("The bot is not playing anything at the moment.")