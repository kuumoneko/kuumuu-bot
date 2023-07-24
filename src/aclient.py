from kuumuu_import import *



scope = "user-library-read"

config_dir = os.path.abspath(f"{__file__}/../../")
prompt_name = 'kuumuu_data/system_prompt.txt'
prompt_path = os.path.join(config_dir, prompt_name)


sys.path.append('D:\\')

# import somedata.config
sys.path.append(os.path.abspath(os.path.join( os.path.pardir , 'data_base')))
# print (sys.path)
import config
# import client_secret_CLIENTID

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def def_value():
    return "Not present"
    
music_queue = defaultdict(def_value)
    

class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(intents=intents)

        self.client = discord.Client(intents= intents)
        self.bot = commands.Bot(command_prefix=';' , intents= intents)
        
        
        self.music = Music_command.Music(client= self)
        self.support = Support_command.Support(client= self)
        self.ulti = Ultility_command.Ulitlity(client= self)
        self.ai = AI_command.AI(client= self)
        self.mod  = Moderator_command.Moderator(client= self)
  
        self.load_extension = self.bot.load_extension
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(
            type=discord.ActivityType.streaming, name="with kuumo:3")


kuumoclient = aclient()

