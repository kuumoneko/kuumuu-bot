from kuumuu_bot import *
from main_bot.support import *

class Select_command(Select):
    def __init__(self, options):

        super().__init__(placeholder="Select", custom_id="test", options=options, max_values=1)

    # reply 
    async def callback(self, interaction: discord.Interaction):
        
        # print(self.values)
        embed = discord.Embed(description="" , title="" , color= get_kuumo_color(kuumo_color))
        # print(type(int(self.values[0]) ))
        
        kuuuuumo = self.values[0]
        temp = int(kuuuuumo)
        
        # print(interaction.guild)
        # print(type(temp) , ' ' , temp)
        
        user : discord.Member
        
        async for i in interaction.guild.bans():
            moi = i.user.id
            if (moi == temp):
                user = i.user
        
    
        embed.add_field(name='' , value=f'{user} was unbaned')
        await interaction.guild.unban(user)
        await interaction.response.send_message(embed= embed, ephemeral=True)
        
        temp = interaction.guild.id
        channel = kclient.get_channel(int(kurru[str(temp)])) # replace with your channel ID
        
        embeb = discord.Embed(title="" , color= get_kuumo_color(kuumo_color))
        embeb.add_field(name ='' ,value= f'{user} was unbaned by {interaction.user}')
        await channel.send(embed= embeb)

class ViewButton(View):
    
    # label: The label of the button which is displayed
    # style: The background color of the button
    @button(label="Unban commands Menu", custom_id= 'Unban' , style= discord.ButtonStyle.blurple , disabled= False)
    async def unban_menu(self, interaction: discord.Interaction , butt_oj = Button):
        await interaction.message.delete()
        # This function is called when a user clicks on the button

        options = []
        async for i in interaction.guild.bans():
            options.append(discord.SelectOption(label=i.user.name, value=i.user.id))
            
        # interaction: discord.Interaction
        # create Select instance and add it to a new view
        select = Select_command(options=options )
        view_select = View()
        view_select.add_item(select)

        # edit the message with the new view
        await interaction.response.send_message(content="Choose an option", view=view_select , ephemeral= True)
        # await interaction.message.delete()
        
async def unban_member(ctx : discord.Interaction ):
    print(ctx.guild)
    await ctx.response.send_message("Click this button to see ban lists!", view= ViewButton() )
    # await ctx.message.delete()