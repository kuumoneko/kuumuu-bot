import os
import re
import sys
import urllib3
import pafy
import pkg_resources
from googletrans import Translator
from random import *
import discord.ext.context
import datetime
import ffmpeg
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import youtube_dl
from discord.utils import get
from time import sleep
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import discord
import asyncio
from collections import defaultdict
from discord import *
from discord.ext import commands
from discord.ext import *
from discord.ext.commands import *
from discord.app_commands import CommandTree
from queue import Queue
from discord.ui import *
from typing import Union, List
from src import log, art, personas, responses
from src import responses
from src.log import logger
from dotenv import load_dotenv
from discord import app_commands
from discord.ext.commands.bot import BotBase
from revChatGPT.V3 import Chatbot
from revChatGPT.V1 import AsyncChatbot
from Bard import Chatbot as BardChatbot
from EdgeGPT.EdgeGPT import Chatbot as EdgeChatbot
from src.auto_login.AutoLogin import MicrosoftBingAutoLogin
from collections import deque

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()



scope = "user-library-read"

config_dir = os.path.abspath(f"{__file__}/../../")
prompt_name = 'kuumuu_data/system_prompt.txt'
prompt_path = os.path.join(config_dir, prompt_name)


sys.path.append('D:\\')

# import somedata.config
sys.path.append(os.path.abspath(os.path.join( os.path.pardir , 'somedata')))
# print (sys.path)
import config
# import client_secret_CLIENTID

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read()
    
    
def def_value():
    return "Not present"
    
music_queue = defaultdict(def_value)
    

class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(intents=intents)

        self.client = discord.Client(intents= intents)
        self.bot = commands.Bot(command_prefix=';' , intents= intents)
        
        ''' Youtube '''
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = "D:/somedata/client_secret_CLIENTID.json"
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        self.client_secrets_file, scopes)
    
        self.credentials = flow.run_local_server()
        self.ytb = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=self.credentials)
        
        
        self.ctrack = defaultdict(self.def_value)
        '''
                In music_current_queue:

                Left Queue  ||  music_current_queue  ||  Right Queue

                  first------------------------------------Second
        '''
        
        self.ptrack = defaultdict(self.def_value)
        '''
                In music_previous_queue:

                Left Queue  ||  music_previous_queue  ||  Right Queue

                  first-------------------------------------Second
        '''
        self.is_loop= defaultdict(self.def_loop)
        
        self.load_extension = self.bot.load_extension
        self.tree = app_commands.CommandTree(self)
        
        self.kuumo_color = list([
                0xCD5C5C,0xFF6A6A,0xEE6363,0xCD5555,0x8B3A3A,0xB22222,0xFF3030,0xEE2C2C,0xCD2626,
                0x8B1A1A,0xA52A2A,0xFF4040,0xEE3B3B,0xCD3333,0x8B2323,0xFF8C00,0xFF7F00,0xEE7600,
                0xCD6600,0xFF6347,0xEE5C42,0xFF4500,0xEE4000,0xFF0000,0xEE0000,0xDC143C   
                ])
        
        self.play_data = defaultdict(self.daata)
        
        self.current_channel = None
        self.activity = discord.Activity(
            type=discord.ActivityType.streaming, name="with kuumo:3")
        self.isPrivate = "False"
        self.is_replying_all = "False"
        self.replying_all_discord_channel_id = "True"

        chrome_version = 114
        
    
        # print(self.spotify_id)
        self.bing_account = config.BING_ACCOUNT
        self.bing_password = config.BING_PASSWORD
        MicrosoftBingAutoLogin(
            self.bing_account, self.bing_password, chrome_version).dump_cookies()

        self.chat_model = "Bing"
        self.chatbot = self.get_chatbot_model()
        self.message_queue = asyncio.Queue()
        
    async def get_color(self):
        mid = randrange(0 , len(self.kuumo_color)-1 , 1)
        kurumu = self.kuumo_color[mid]
        return kurumu
    
    
    def def_value(moi : int):
        return deque([])
    
    def def_loop(moi : int):
        return False
    
    def def_premium(mem : discord.Member):
        return False
    
    def get_id(self , ctx : discord.Interaction):
        return ctx.guild_id
    
    def daata(moi : int):
        return "None"

    async def process_messages(self):
        while True:
            if self.current_channel is not None:
                while not self.message_queue.empty():
                    async with self.current_channel.typing():
                        message, user_message = await self.message_queue.get()
                        try:
                            await self.send_message(message, user_message)
                        except Exception as e:
                            logger.exception(
                                f"Error while processing message: {e}")
                        finally:
                            self.message_queue.task_done()
            await asyncio.sleep(1)

    async def get_all_command(self):
        for i in self.get_all_guilds:
            temp = self.tree._get_all_commands(i)
            print(temp)
            
    async def change_time(self , string : str):
        check_list = ["D" , "H" , "M" , "S"]
        res = ""
        
        for char in check_list:
            temp = string.find(char)
            strtemp = ""
            if temp == -1:
                continue
        
            if (temp != -1):
                strtemp = string[ (temp-3)  : (temp-len(string))   ]
                
            k = len(strtemp)-1
            while(ord(strtemp[k]) >= 48 and ord(strtemp[k]) <= 57 and k > 0 ):
                k-=1

            for i in range (60 , 96):
                strtemp = strtemp.strip(chr(i))
            for i in range(97 , 123):
                strtemp = strtemp.strip(chr(i))
                
            if k != 0:
                strtemp = strtemp[  len(strtemp) - k  :  ]
            
            if strtemp != "":
                if (char == "D"):
                    res += strtemp + " days "
                if (char == "H"):
                    res += strtemp + " hours "
                if (char == "M"):
                    res += strtemp + " minutes "
                if (char == "S"):
                    res += strtemp + " seconds "
        
        return res

    async def add_to_queue(self , ctx: discord.Interaction , url: str = None , query: str = None , list_url:str = None):
        embeb = discord.Embed(title="" , color= await self.get_color())
        
        if query != None:
            lists = []
        
            request = self.ytb.search().list(
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
                request1 = self.ytb.videos().list(
                            part="snippet,contentDetails,statistics",
                            id=j['id']['videoId']
                        )

                embeb1 = discord.Embed(title=f"Track's info" , color= await self.get_color())
                response1 = request1.execute()
                i = response1["items"][0]
                
                link = i['id']

                embeb1.set_thumbnail(url= i['snippet']['thumbnails']['default']['url'])

                embeb1.add_field(name="Track's Name: " , value= i['snippet']['title'] , inline= True)
                embeb1.add_field(name="Link:" , value=link , inline= True)
                embeb1.add_field(name="Channel: " , value=  i['snippet']['channelTitle'] , inline= False )

                embeb1.add_field(name="Viewers: " , value= i['statistics']['viewCount'] , inline= True)
                embeb1.add_field(name="Likers: " , value= i['statistics']['likeCount'] , inline= True)

                embeb1.add_field(name="Duration: " , value=await self.change_time(i['contentDetails']['duration']) , inline= True)
                
                lists.append(embeb1)
                if (cnt == 5):
                    break
                
            await ctx.channel.send(view= Search( ctx= ctx , client= self ,result= lists) )
        
            
            return
            
        elif url != None:
            self.ctrack[ctx.guild_id].append(url[len(url) - 11:])
            embeb1 = Embed(title=f"Track's info" , color=await self.get_color())
            embeb1.add_field(name="" , value=f"Track have been added to queue")

            await ctx.channel.send(embed= embeb1)
            return
        
        elif list_url != None:
            embeb1 = Embed(title=f"Track's info" , color=await self.get_color())

            URL = list_url[list_url.find('=') + 1 : ]
            
            request = self.ytb.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=100,
                playlistId= URL
            )
            response = request.execute()
            
            temp = response.get('nextPageToken' , None)
            cnt=0

            while(temp != None):
                for i in response['items']:
                    if i['snippet']['title'] != 'Deleted video' and i['snippet']['title'] != "Private video":
                        kuumoclient.ctrack[ctx.guild_id].append(i['snippet']['resourceId']['videoId'])
                        cnt+=1
                        
                request = self.ytb.playlistItems().list(
                    part="snippet,contentDetails",
                    maxResults=100,
                    pageToken= temp,
                    playlistId= URL
                    )
                response = request.execute() 
                temp = response.get('nextPageToken', None)

            for i in response['items']:
                if i['snippet']['title'] != 'Deleted video' and i['snippet']['title'] != "Private video":
                    self.ctrack[ctx.guild_id].append(i['snippet']['resourceId']['videoId'])
                    cnt+=1
                        
            # embeb1.add_field(name="Warning: " , value=f"The feature is not currently activated. Please contact <@950354453033263175> or `mod` for assistance")
            embeb1.add_field(name="" , value=f"{cnt} tracks have been added to queue")
            await ctx.channel.send(embed= embeb1)
            return
        else:
            embeb.add_field(name="Warning:" , value=f'Please use youtube_url or query to search on youtube!')
            await ctx.channel.send(embed= embeb)
            return
        
    async def connecting(self , ctx : discord.Interaction):
        voice_clientt : VoiceClient
        channel = ctx.user.voice.channel
        voice_clientt = discord.utils.get(self.voice_clients, guild=ctx.guild)
        if not voice_clientt is None:
            if not voice_clientt.is_connected():
                voice_clientt = await channel.connect()
        else:
            voice_clientt = await channel.connect() 
        return voice_clientt

    async def play(self , ctx : discord.Interaction , id:int):
        '''
            pramater:
                id : should be Member.id or Guild.id
        '''
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        voice_clientt = await self.connecting(ctx= ctx)
        
        if voice_clientt.is_playing():
            return
        
        curr_list = self.ctrack[id]
        pre_list = self.ptrack[id]
            
        while len(curr_list) != 0:

            if(voice_clientt.is_connected() == False):
                return

            url = curr_list[0]
            
            # print(curr_list)
            # print(pre_list)
            
            temp = "https://www.youtube.com/watch?v="+url
            
            song = pafy.new(url=temp)  # creates a new pafy object
            audio = song.getbestaudio()  # gets an audio source
            tempp = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
            
            
            
            while voice_clientt.is_playing() or voice_clientt.is_paused():
                await asyncio.sleep(1.0)   
                
            voice_clientt.play(tempp)
            
            embeb1 = Embed(title=f"Track's info" , color=await self.get_color())
            request = self.ytb.videos().list(
                part="snippet,contentDetails,statistics",
                id=url
            )
            response =  request.execute()
            i = response["items"][0]
            
            embeb1.set_thumbnail(url= i['snippet']['thumbnails']['default']['url'])

            embeb1.add_field(name="Track's Name: " , value= i['snippet']['title'] , inline= True)
            embeb1.add_field(name="Channel: " , value=  i['snippet']['channelTitle'] , inline= False )

            embeb1.add_field(name="Viewers: " , value= i['statistics']['viewCount'] , inline= True)
            embeb1.add_field(name="Likers: " , value= i['statistics']['likeCount'] , inline= True)

            embeb1.add_field(name="Duration: " , value=await self.change_time(i['contentDetails']['duration']) , inline= True)
            
            await ctx.channel.send(embed= embeb1)
            
            await asyncio.sleep(3.0)
            while voice_clientt.is_playing() or voice_clientt.is_paused():
                await asyncio.sleep(1.0)
            
            if len(curr_list)>0:
                if self.is_loop[id] == False:
                    pre_list.append(curr_list[0])
                else:
                    curr_list.append(curr_list[0])
                curr_list.popleft()    
                
            curr_list = self.ctrack[id]   
        return
    
    async def next_track(self , ctx : discord.Interaction , id:int):
        '''
            pramater:
                id : must be Member.id or Guild.id
        '''
        voice_clientt = await self.connecting(ctx= ctx)
    
        voice_clientt.stop()
            
        curr_list = self.ctrack[id]
        pre_list = self.ptrack[id]
        
        if self.is_loop[id] == False:
            pre_list.append(curr_list[0])
        else:
            curr_list.append(curr_list[0])
        curr_list.popleft()   
        
        await self.play(ctx= ctx , id= id)
    
    async def previous_track(self , ctx : discord.Interaction , id:int):
        voice_clientt = await self.connecting(ctx= ctx)
    
        voice_clientt.stop()
            
            
        curr_list = self.ctrack[id]
        pre_list = self.ptrack[id]
        
        if self.is_loop[id] == False:  
            curr_list.appendleft(pre_list[-1])
            pre_list.pop()
        else:
            curr_list.appendleft(curr_list[-1])
            curr_list.pop()   
            
        await self.play(ctx= ctx , id= id)
            
    
    async def stop_music(self , ctx: discord.Interaction , id : int):
        voice_clientt = await self.connecting(ctx= ctx)
        if (voice_clientt.is_playing()):
            voice_clientt.stop()
            
        while( len (self.ctrack[id]) > 0):
            self.ctrack[id].popleft()
            
        while( len (self.ptrack[id]) > 0):
            self.ptrack[id].popleft()
        
        return   
    
    async def pause_music(self , ctx: discord.Interaction):
        voice_clientt = await self.connecting(ctx= ctx) 
        if voice_clientt.is_playing():
            voice_clientt.pause()

        
    async def resume_music(self , ctx: discord.Interaction):
        voice_clientt = await self.connecting(ctx= ctx)
        if voice_clientt.is_paused():
            voice_clientt.resume()
    
    async def join(self, ctx:discord.Interaction):
        channel = ctx.user.voice.channel
        await channel.connect()

    async def leave(self , ctx : discord.Interaction):
        channel = ctx.guild.voice_client
        await channel.disconnect()

    def get_chatbot_model(self, prompt=prompt) -> Union[AsyncChatbot, Chatbot]:
        cookies = json.loads(open("./cookies.json", encoding="utf-8").read())
        return EdgeChatbot(cookies=cookies)

    async def process_messages(self):
        while True:
            if self.current_channel is not None:
                while not self.message_queue.empty():
                    async with self.current_channel.typing():
                        message, user_message = await self.message_queue.get()
                        try:
                            await self.send_message(message, user_message)
                        except Exception as e:
                            logger.exception(
                                f"Error while processing message: {e}")
                        finally:
                            self.message_queue.task_done()
            await asyncio.sleep(1)

    async def get_all_command(self):
        # /self.get_all_members
        for i in self.get_all_guilds:
            temp = self.tree._get_all_commands(i)
            print(temp)

    async def enqueue_message(self, message, user_message):
        await message.response.defer(ephemeral=self.isPrivate) if self.is_replying_all == "False" else None
        await self.message_queue.put((message, user_message))

    async def send_message(self, message, user_message):
        if self.is_replying_all == "False":
            author = message.user.id
        else:
            author = message.author.id
        try:
            response = (f'> **{user_message}** - <@{str(author)}> \n\n')

            response = f"{response}{await responses.bing_handle_response(user_message, self)}"
            char_limit = 1900
            if len(response) > char_limit:
                # Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
                if "```" in response:
                    # Split the response if the code block exists
                    parts = response.split("```")

                    for i in range(len(parts)):
                        if i % 2 == 0:  # indices that are even are not code blocks
                            if self.is_replying_all == "True":
                                await message.channel.send(parts[i])
                            else:
                                await message.followup.send(parts[i])
                        else:  # Odd-numbered parts are code blocks
                            code_block = parts[i].split("\n")
                            formatted_code_block = ""
                            for line in code_block:
                                while len(line) > char_limit:
                                    # Split the line at the 50th character
                                    formatted_code_block += line[:char_limit] + "\n"
                                    line = line[char_limit:]
                                formatted_code_block += line + "\n"  # Add the line and seperate with new line

                            # Send the code block in a separate message
                            if (len(formatted_code_block) > char_limit+100):
                                code_block_chunks = [formatted_code_block[i:i+char_limit]
                                                     for i in range(0, len(formatted_code_block), char_limit)]
                                for chunk in code_block_chunks:
                                    if self.is_replying_all == "True":
                                        await message.channel.send(f"```{chunk}```")
                                    else:
                                        await message.followup.send(f"```{chunk}```")
                            elif self.is_replying_all == "True":
                                await message.channel.send(f"```{formatted_code_block}```")
                            else:
                                await message.followup.send(f"```{formatted_code_block}```")
                else:
                    response_chunks = [response[i:i+char_limit]
                                       for i in range(0, len(response), char_limit)]
                    for chunk in response_chunks:
                        if self.is_replying_all == "True":
                            await message.channel.send(chunk)
                        else:
                            await message.followup.send(chunk)
            elif self.is_replying_all == "True":
                await message.channel.send(response)
            else:
                await message.followup.send(response)
        except Exception as e:
            if self.is_replying_all == "True":
                await message.channel.send(f"> **ERROR: Something went wrong, please try again later!** \n ```ERROR MESSAGE: {e}```")
            else:
                await message.followup.send(f"> **ERROR: Something went wrong, please try again later!** \n ```ERROR MESSAGE: {e}```")
            logger.exception(f"Error while sending message: {e}")

    async def send_start_prompt(self):
        import os.path

        config_dir = os.path.abspath(f"{__file__}/../../")
        prompt_name = 'other_file/txt_file/system_prompt.txt'
        prompt_path = os.path.join(config_dir, prompt_name)
        discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")
        try:
            if os.path.isfile(prompt_path) and os.path.getsize(prompt_path) > 0:
                with open(prompt_path, "r", encoding="utf-8") as f:
                    prompt = f.read()
                    if (discord_channel_id):
                        logger.info(
                            f"Send system prompt with size {len(prompt)}")
                        response = ""

                        response = f"{response}{await responses.bing_handle_response(prompt, self)}"
                        channel = self.get_channel(int(discord_channel_id))
                        await channel.send(response)
                        logger.info(f"System prompt response:{response}")
                    else:
                        logger.info(
                            "No Channel selected. Skip sending system prompt.")
            else:
                logger.info(f"No {prompt_name}. Skip sending system prompt.")
        except Exception as e:
            logger.exception(f"Error while sending system prompt: {e}")


kuumoclient = aclient()



class Search_video(discord.ui.Select):
    def __init__(self ,ctx : discord.Interaction, result : List):
        self.kuumo = result
        self.ctx =ctx
        
        options = [
            discord.SelectOption(label='1', description='The first Video'  , value= 1),
            discord.SelectOption(label='2', description='The second video' , value= 2),
            discord.SelectOption(label='3', description='The Third video'  , value= 3),
            discord.SelectOption(label='4', description='The 4th video'    , value= 4),
            discord.SelectOption(label='5', description='The 5th video'    , value= 5),
        ]

        super().__init__(placeholder='Select other page to see other track for selecting your track to play', min_values=1, max_values=1, options=options )

    async def callback(self, interaction: discord.Interaction ):
        await interaction.response.edit_message(embed= self.kuumo[ord(self.values[0]) - 49])
        
class Search(discord.ui.View):
    def __init__(self , client : aclient , ctx : discord.Interaction, result : List):
        super().__init__(timeout=180)
        self.result = result
        self.music = client
        
    async def chosen(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button) or isinstance(child , discord.ui.Select):
                child.disabled = True
        
    @discord.ui.select(placeholder='Select other page to see other track for selecting your track to play', min_values=1, max_values=1, 
                       options=[
                           discord.SelectOption(label='1', description='The first Video'  , value= 1),
                            discord.SelectOption(label='2', description='The second video' , value= 2),
                            discord.SelectOption(label='3', description='The Third video'  , value= 3),
                            discord.SelectOption(label='4', description='The 4th video'    , value= 4),
                            discord.SelectOption(label='5', description='The 5th video'    , value= 5),
                       ] )
    async def select_callback(self, interaction : discord.Interaction , select): # the function called when the user is done selecting options
        await interaction.response.edit_message(embed= self.result[ ord(select.values[0]) - 49 ])
        
    @discord.ui.button(label="Track 1", custom_id= "1" ,  style=discord.ButtonStyle.primary)
    async def first_button_callback(self,  interaction : discord.Interaction , button : ui.Button):
        self.music.ctrack[interaction.guild].append(self.result[0].fields[1].value)
        await interaction.response.send_message(embed=self.result[0])
        self.stop()
    
    @discord.ui.button(label="Track 2", custom_id= "2" ,  style=discord.ButtonStyle.primary)
    async def second_button_callback(self,  interaction : discord.Interaction , button):
        self.music.ctrack[interaction.guild].append(self.result[1].fields[1].value)
        await interaction.response.send_message(embed=self.result[1])
        self.stop()
        
    @discord.ui.button(label="Track 3", custom_id= "3" ,  style=discord.ButtonStyle.primary)
    async def third_button_callback(self,  interaction : discord.Interaction , button):
        self.music.ctrack[interaction.guild].append(self.result[2].fields[1].value)
        await interaction.response.send_message(embed=self.result[2])
        self.stop()

    @discord.ui.button(label="Track 4", custom_id= "4" ,  style=discord.ButtonStyle.primary)
    async def four_button_callback(self,  interaction : discord.Interaction , button):
        self.music.ctrack[interaction.guild].append(self.result[3].fields[1].value)
        await interaction.response.send_message(embed=self.result[3])
        self.stop()
        
    @discord.ui.button(label="Track 5", custom_id= "5" ,  style=discord.ButtonStyle.primary)
    async def five_button_callback(self,  interaction : discord.Interaction , button):
        self.music.ctrack[interaction.guild].append(self.result[4].fields[1].value)
        await interaction.response.send_message(embed=self.result[4])
        self.stop()