from src.video import *
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
    # ensure there is a player_manager when creating a new voice_client
    await channel.disconnect()
    # temp = channel.channel
    
    await ctx.response.send_message(f'{kclient.user.name} has been disconnected from <#{channel.channel.id}>')    


async def play_music(ctx: discord.Interaction , url: str = None , query: str = None):
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
        lists = []
    
        request = kclient.ytb.search().list(
            part="snippet",
            maxResults=10,
            q= query
        )
        cnt =0

        response = request.execute()

        for j in response["items"]:

            if j['id']['kind'] != 'youtube#video':
                continue

            cnt+=1
            request1 = kclient.ytb.videos().list(
            part="snippet,contentDetails,statistics",
            # id="5qap5aO4i9A"
            id=j['id']['videoId']
            )

            embeb = discord.Embed(title=f"Track's info" , color=0xFF6A6A)
            response1 = request1.execute()
            i = response1["items"][0]
            
            link = "https://youtu.be/" + i['id']

            embeb.set_thumbnail(url= i['snippet']['thumbnails']['default']['url'])

            embeb.add_field(name="Track's Name: " , value= i['snippet']['title'] , inline= True)
            embeb.add_field(name="Link:" , value=link , inline= True)
            embeb.add_field(name="Channel: " , value=  i['snippet']['channelTitle'] , inline= False )

            embeb.add_field(name="Viewers: " , value= i['statistics']['viewCount'] , inline= True)
            embeb.add_field(name="Likers: " , value= i['statistics']['likeCount'] , inline= True)

            embeb.add_field(name="Duration: " , value= change_time(i['contentDetails']['duration']) , inline= True)
            # embeb

            
            lists.append(embeb)
            if (cnt == 5):
                break
            
        await ctx.response.send_message(view= Search( ctx= ctx , result= lists) )
        
        
        # music_current_queue[ctx.guild].append(url)
        
        
        return
        
    elif url != None:
        embeb = Embed(title=f"Track's info" , color=get_kuumo_color(kuumo_color))
        request = kclient.ytb.videos().list(
            part="snippet,contentDetails,statistics",
            id=url[len(url) -11:]
        )
        response =  request.execute()

        i = response["items"][0]
        embeb.set_thumbnail(url= i['snippet']['thumbnails']['default']['url'])

        embeb.add_field(name="Track's Name: " , value= i['snippet']['title'] , inline= True)
        embeb.add_field(name="Channel: " , value=  i['snippet']['channelTitle'] , inline= False )

        embeb.add_field(name="Viewers: " , value= i['statistics']['viewCount'] , inline= True)
        embeb.add_field(name="Likers: " , value= i['statistics']['likeCount'] , inline= True)

        embeb.add_field(name="Duration: " , value= change_time(i['contentDetails']['duration']) , inline= True)

        music_current_queue[ctx.guild].append(url)
        await ctx.response.send_message(embed=embeb)
        return
    else:
        embeb.add_field(name="Warning:" , value=f'Please use youtube_url or query to search on youtube!')
        await ctx.response.send_message(embed= embeb)
        return
    
    
async def pause_music(ctx: discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)

    print("voice_clientt ", voice_clientt.is_playing() , " playing")
    
    if voice_clientt.is_playing():
        voice_clientt.pause()
    
    return

    
async def resume_music(ctx: discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)
    
    if voice_clientt.is_paused():
        voice_clientt.resume()
    
    return
  
async def stop_music(ctx: discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)
    if (voice_clientt.is_playing()):
        voice_clientt.stop()
        
    while( len (music_current_queue[ctx.guild]) > 0):
        music_current_queue[ctx.guild].popleft()
        
    while( len (music_previous_queue[ctx.guild]) > 0):
        music_previous_queue[ctx.guild].popleft()
    
    return   
    
async def next_track(ctx: discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)
    
    if voice_clientt.is_playing():
        voice_clientt.pause()
    
    music_previous_queue[ctx.guild].append(music_current_queue[ctx.guild][0])
    music_current_queue[ctx.guild].popleft()
    if voice_clientt.is_paused():
        voice_clientt.resume()
        voice_clientt.stop()
        await playing_music(ctx)
        
    return

async def previous_track(ctx : discord.Interaction):
    voice_clientt = await connecting(ctx= ctx)
    if voice_clientt.is_playing():
        voice_clientt.pause()
        
    music_current_queue[ctx.guild].appendleft(music_previous_queue[ctx.guild][-1])
    music_previous_queue[ctx.guild].pop()
    
    if voice_clientt.is_paused():
        voice_clientt.resume()
        voice_clientt.stop()
        await playing_music(ctx)
        
    return