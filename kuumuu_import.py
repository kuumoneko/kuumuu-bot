import os
import re
import sys
import urllib3
import pafy
import pkg_resources
from googletrans import Translator
from random import *
import discord.ext.commands
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
from discord import app_commands
from discord.ext.commands.bot import BotBase
from revChatGPT.V3 import Chatbot
from revChatGPT.V1 import AsyncChatbot
from EdgeGPT.EdgeGPT import Chatbot as EdgeChatbot
from src.auto_login.AutoLogin import MicrosoftBingAutoLogin
from collections import deque
from typing import List
from datetime import *

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials


from all_command import *