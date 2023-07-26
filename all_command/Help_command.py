from kuumuu_import import *

# from src.aclient import aclient
class Help():
    def __init__(self , client  ) -> None:
        
        self.__client__ = client
        
        self.mod = self.__client__.mod
        self.ulti = self.__client__.ulti
        self.ai = self.__client__.ai
        self.music = self.__client__.music
        
        self.helped = [
                self.mod,
                self.ulti,
                self.ai,
                self.music
            ]
        
        self.kuumo_help={
                self.mod : "Moderation",
                self.ulti : "Ultility",
                self.ai : "AI chat",
                self.music: "Music"
        }
        
        super().__init__()
        
    async def help(self , ctx : discord.Interaction , command):
        await ctx.response.defer(thinking=True)
        if command == None:
            
            kuumo_embed = Embed(title="Kuumuu Command Help" , color=self.__client__.support.get_kuumo_color())
            kuumo_embed.set_thumbnail(url= ctx.user.avatar.url)

            
            for group in self.helped:
                kuumo_string = ""
                                
                for commanda in dir(group):
                    
                    if commanda[0] != "_":
                        kuumo_command : Command
                        kuumo_command = self.__client__.tree.get_command(commanda)
                    
                        kuumo_string = kuumo_string + f"`{kuumo_command.name}` "
                
                kuumo_embed.add_field(name=f'{self.kuumo_help[group]}:' , value=kuumo_string  , inline=False)
            
            await ctx.followup.send(embed= kuumo_embed)
        
            
        else:
            kuumo_embed = Embed(title="Kuumuu Command Help" , color=self.__client__.support.get_kuumo_color())
            kuumo_embed.set_thumbnail(url= ctx.user.avatar.url)
            
            # temp : Command
            temp = self.__client__.tree.get_command(command)
            # print(f'  {temp.name}:')
            
            parama = ""
            
            kuumo_parame = ""
            
            if len(temp._params) == 0:
                kuumo_parame = f"This command don't have parameter"
                parama = f""
                
            else:
                for pram in temp._params:
                    lenght = len(pram)
                    temp_length = 12 - lenght - 3
                    
                    parama = parama + " {" + f"{pram}" + "} "
                    
                    kuumo_parame = kuumo_parame + f"  {pram}:     {temp._params[pram].description.message}\n"
                    
                    
            
            kuumo_embed.add_field(name=f'Overview:' , value=f'```  {command}: {parama}```' , inline=False)
            
            kuumo_embed.add_field(name=f"Description:" , value=f"```  {temp.description}```")
            
            kuumo_embed.add_field(name=f"Parameters:" , value=f"```{kuumo_parame}```" , inline= False)
            
            await ctx.followup.send(embed=kuumo_embed)
