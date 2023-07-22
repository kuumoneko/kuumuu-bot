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
        
        
        self.music = Music_command.Music(client= self)
        self.support = Support_command.Support(client= self)
        self.ulti = Ultility_command.Ulitlity(client= self)
        self.ai = AI_command.AI(client= self)
        
        
        ''' Youtube '''
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.client_secrets_file = "D:/data_base/client_secret_CLIENTID.json"
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
        
        self.activity = discord.Activity(
            type=discord.ActivityType.streaming, name="with kuumo:3")


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

kuumoclient = aclient()

