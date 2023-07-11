from src.aclient import *
from kuumuu_bot import music_current_queue 

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
    def __init__(self ,ctx : discord.Interaction, result : List):
        super().__init__(timeout=180)
        self.result = result
        
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
        music_current_queue[interaction.guild].append(self.result[0].fields[1].value)
        await interaction.response.send_message(embed=self.result[0])
        self.stop()
    
    @discord.ui.button(label="Track 2", custom_id= "2" ,  style=discord.ButtonStyle.primary)
    async def second_button_callback(self,  interaction : discord.Interaction , button):
        music_current_queue[interaction.guild].append(self.result[1].fields[1].value)
        await interaction.response.send_message(embed=self.result[1])
        self.stop()
        
    @discord.ui.button(label="Track 3", custom_id= "3" ,  style=discord.ButtonStyle.primary)
    async def third_button_callback(self,  interaction : discord.Interaction , button):
        music_current_queue[interaction.guild].append(self.result[2].fields[1].value)
        await interaction.response.send_message(embed=self.result[2])
        self.stop()

    @discord.ui.button(label="Track 4", custom_id= "4" ,  style=discord.ButtonStyle.primary)
    async def four_button_callback(self,  interaction : discord.Interaction , button):
        music_current_queue[interaction.guild].append(self.result[3].fields[1].value)
        await interaction.response.send_message(embed=self.result[3])
        self.stop()
        
    @discord.ui.button(label="Track 5", custom_id= "5" ,  style=discord.ButtonStyle.primary)
    async def five_button_callback(self,  interaction : discord.Interaction , button):
        music_current_queue[interaction.guild].append(self.result[4].fields[1].value)
        await interaction.response.send_message(embed=self.result[4])
        self.stop()