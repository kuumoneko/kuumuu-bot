import os
import re
import sys
import urllib3
import pafy
import pkg_resources
from googletrans import Translator
import discord.ext.context
from lavalink.filters import LowPass
import datetime
import ffmpeg
from lavalink.playermanager import *
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import youtube_dl
from discord.utils import get
from time import sleep
import json
import discord
import asyncio
import lavalink
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
from kuumuu_data.config import *

load_dotenv()

scope = "user-library-read"

config_dir = os.path.abspath(f"{__file__}/../../")
prompt_name = 'kuumuu_data/system_prompt.txt'
prompt_path = os.path.join(config_dir, prompt_name)
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
        
        
        self.load_extension = self.bot.load_extension
        self.tree = app_commands.CommandTree(self)
        
        self.lavalink = lavalink.Client
        
        self.current_channel = None
        self.activity = discord.Activity(
            type=discord.ActivityType.listening, name="/chat | /help")
        self.isPrivate = "False"
        self.is_replying_all = "False"
        self.replying_all_discord_channel_id = "True"

        chrome_version = 114
        
    
        # print(self.spotify_id)
        self.bing_account = BING_ACCOUNT
        self.bing_password = BING_PASSWORD
        MicrosoftBingAutoLogin(
            self.bing_account, self.bing_password, chrome_version).dump_cookies()

        self.chat_model = "Bing"
        self.chatbot = self.get_chatbot_model()
        self.message_queue = asyncio.Queue()

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
