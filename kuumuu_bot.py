# ---------- đây là các setup của bot ----------

# import discord
from collections import defaultdict
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


