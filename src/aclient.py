from kuumuu_import import *

scope = "user-library-read"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

class aclient(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.TOKEN = config.kuumuu_TOKEN
        
        self.Secure_1PSID = config.Secure_1PSID

        self.Secure_1PSIDTS = config.Secure_1PSIDTS
        
        self.client = discord.Client(intents= intents)
        self.bot = commands.Bot(command_prefix=';' , intents= intents)
        
        
        self.music = Music_command.Music(client= self)
        self.support = Support_command.Support(client= self)
        self.ulti = Ultility_command.Ulitlity(client= self)
        self.ai = AI_command.AI(client= self)
        self.mod  = Moderator_command.Moderator(client= self)
        
        self.help = Help_command.Help(client= self)

        self.load_extension = self.bot.load_extension
        self.tree = app_commands.CommandTree(self)
        self.activity = discord.Activity(
            type=discord.ActivityType.streaming, name="with kuumo:3")
