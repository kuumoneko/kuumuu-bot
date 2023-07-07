# ---------- đây là các setup của bot ----------

# import discord
from collections import defaultdict,deque
from main_bot.support import *
from src.aclient import *
import openai
from main_bot.keep_alive import *
from datetime import *
# import src.personas
# from src.personas import PERSONAS
import sys
from pkg_resources import PkgResourcesDeprecationWarning
# import D.somedata

#---------- Note: 0x = # ----------
prefix = ";"
kclient= kuumoclient
# client = discord.Client(command_prefix=';' , intents= discord.Intents.all())
# kclient = commands.Bot(command_prefix=';' , intents= discord.Intents.all())

emoji = defaultdict(def_value)
emoji = emoji_temp

check_time = get_name_of_time()
timee = get_time()

notifi_room = defaultdict(def_value)
notifi_room = kurru

def moi():
  return deque([])

music_current_queue = defaultdict(moi)
'''
    In music_current_queue:
    
    Left Queue  ||  music_current_queue  ||  Right Queue
    
      first------------------------------------Second
'''

music_previous_queue = defaultdict(moi)
'''
    In music_previous_queue:
    
    Left Queue  ||  music_previous_queue  ||  Right Queue
    
      first-------------------------------------Second
'''


