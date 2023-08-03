from typing import Any, Optional

from discord.enums import TextStyle
from discord.interactions import Interaction
from discord.utils import MISSING
from kuumuu_import import *

# from src.aclient import aclient

class Moderator():
    def __init__(self , client) -> None:
        self.__client__ = client
        
        super().__init__()
        

    async def ban(self , ctx : discord.Interaction, member: discord.Member , reason = None):
        
        if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
            
            embeb = discord.Embed(title='' , color= self.__client__.support.get_kuumo_color())
            
            messageok = f"{member} đã bị ban bởi {ctx.user.name} với lý do {reason}"
            
            embeb.add_field(name='' , value= messageok)
            await member.send(embed= embeb)
            await ctx.response.send_message(embed=embeb)
            await member.ban(reason=reason)
        else:
            raise MissingPermissions()
        
    async def timeout(self , ctx :discord.Interaction , member:discord.Member , numb:int , string):
        if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
            embed=discord.Embed(title="", description="", color=self.__client__.support.get_kuumo_color()) 
            chara = string.value
            val = f'{member} has been timeouted by {ctx.user} in {numb} {string.name}'
                
            embed.add_field(name="", value=val, inline=False)
            
            await ctx.response.send_message(embed=embed)
            if chara == "sec" or chara.startswith('second') :
                await member.timeout( timedelta(seconds= numb))
            elif chara == "min" or chara.startswith('minute'):
                await member.timeout(timedelta(minutes= numb) ) 
            elif chara == "hou" or chara.startswith('hour'):
                await member.timeout( timedelta(hours= numb) ) 
            elif chara == "ds" or chara.startswith('day'):
                await member.timeout( timedelta(days= numb) ) 
            elif chara == "we" or chara.startswith('week'):
                await member.timeout( timedelta(weeks= numb) )
                
            await ctx.response.send_message(embed= embed) 

        else:
            raise MissingPermissions()
            
    async def untimeout(self , ctx : discord.Interaction, member: discord.Member):
        if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
            emmeb = discord.Embed(title='' , color= self.__client__.support.get_kuumo_color())
            emmeb.add_field(name='' , value=f'{member} has been untimeout by {ctx.user}')
            await ctx.response.send_message(embed=emmeb)
            await member.untimeout()
        else:
            raise MissingPermissions()

    async def kick(self , ctx : discord.Interaction, member: discord.Member  ):
        
        if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
            await member.kick()
            emmeb = discord.Embed(title='' , color= self.__client__.support.get_kuumo_color())
            emmeb.add_field(name='' , value=f'{member} has been kicked by {ctx.user}')
            await ctx.response.send_message(embed= emmeb)
        else:
            raise MissingPermissions()

    async def chnick(self , ctx : discord.Interaction, member: discord.Member , name : str):
        if (member == ctx.user and ctx.permissions.manage_nicknames):
            await member.edit(nick= name)
            await ctx.response.send_message(f'Done' , ephemeral= True)
        elif ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role and ctx.permissions.manage_nicknames:
            await member.edit(nick= name)
            await ctx.response.send_message(f'Done' , ephemeral= True)
        else:
            raise MissingPermissions()
        
    async def chrole(self , ctx: discord.Interaction, member:discord.Member , role: discord.Role):
        if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.response.send_message(f'Done' , ephemeral= True)
            else:
                await member.add_roles(role)
                await ctx.response.send_message(f'Done' , ephemeral= True)
        else:
            raise MissingPermissions()
        
    async def warn(self , ctx : discord.Interaction , member : discord.Member , reason : str):
        await member.send(f"You have been warned by {ctx.user.name}, reason: {reason}")
        await ctx.response.send_message(content=f"{member.name} has been warned by you, reason: {reason}" , ephemeral=True)
        
    
        
    async def unban(self , ctx: discord.Interaction):
        
        # await ctx.response.defer(thinking=True)
        lmao = []
    
        async for i in ctx.guild.bans():
            lmao.append(i)
        
        tempp = ViewButton(client= self.__client__ , ctx= ctx , list= lmao )
        
        
        await ctx.response.send_message(view= tempp)
        await temp(self= tempp , ctx= ctx)

class input(TextInput):
    def __init__(self , client) -> None:
        self.client = client
         
        
        super().__init__(label="" , style= TextStyle.short , custom_id="input bans", placeholder="Input Your Chõie")
        
    async def call_back(self, interaction: discord.Interaction):
        self.client.done = True
        print("Done")
        # return await super().callback(interaction)
        
class ViewButton(View):
    def __init__(self, client : Moderator , ctx : discord.Interaction , list:list , timeout: float | None = 180):
        self.__client__ = client
        self.ctx = ctx
        self.done = False
        self.curr_page = 0
        # self.sp = sp
        
        self.bans = list
        
        
        self.bans_numb = len(self.bans)
        self.page = self.bans_numb // 10 -1  if self.bans_numb % 10 == 0 else self.bans_numb//10 
        
        
        self.bans_page = self.get_options(self.ctx)
        
        super().__init__(timeout=timeout)
        
        # self.add_item(input(client= self))
        
    def get_options(self , ctx : discord.Interaction):
        lists = []
                
        i = 0
        while(i < self.bans_numb):
            embed = Embed(title="" , color= self.__client__.support.get_kuumo_color())
            if (i % 10 == 0):
                embed.add_field(name=" ", value=f'{i % 10 + 1}. {self.bans[i].user}' , inline= True)
                i=i+1
                while(i % 10 != 0):
                    if i == self.bans_numb:
                        break
                    embed.add_field(name="" , value=f'{i % 10 + 1}. {self.bans[i].user}' , inline= True)
                    i=i+1
                
            lists.append(embed)
        
        return lists

    
    @button(label="<" , custom_id="<" , style= discord.ButtonStyle.blurple)
    async def previous_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = self.curr_page - 1

    @button(label=">" , custom_id=">" , style= discord.ButtonStyle.blurple)
    async def next_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = self.curr_page + 1
    
    @button(label="<<" , custom_id="<<" , style= discord.ButtonStyle.blurple )
    async def begin_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = self.page
        
    
    @button(label=">>" , custom_id=">>" , style= discord.ButtonStyle.blurple )
    async def end_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = 0
        
    @select(placeholder="Choose your choice" , custom_id="input" , min_values=1 , max_values=1 ,options=[
                                                                                discord.SelectOption(label="1" , value= "1"),
                                                                                discord.SelectOption(label="2" , value= "2"),
                                                                                discord.SelectOption(label="3" , value= "3"),
                                                                                discord.SelectOption(label="4" , value= "4"),
                                                                                discord.SelectOption(label="4" , value= "5")                   
                                                                                        ])
    async def input(self , ctx : discord.Interaction , select):
        
        moi = (ord(select.values[0]) - ord('1'))
        
        temp = self.bans_page[self.curr_page].fields[moi].value[3:]
        
        
        # print(temp)
        
        async for i in ctx.guild.bans():
            if i.user.name == temp:
                kuumo = Embed(title="" , color= self.__client__.support.get_kuumo_color())
                kuumo.add_field(name="" , value=f"{i.user} has been unbaned by {ctx.user}")
                await ctx.channel.send(embed=kuumo)

                await ctx.guild.unban(i.user)
                break
        self.done = True
        pass
    
async def temp(self : ViewButton, ctx : discord.Interaction):
        
    while(self.done == False):
        # print((self.curr_page == 0) , ' ' , (self.curr_page == self.page) , ' ' , self.previous_page.disabled , ' ' , self.next_page.disabled , ' ' , self.begin_page.disabled , ' ' , self.end_page.disabled)
        
        if self.curr_page == 0:
            self.previous_page.disabled = True
            self.begin_page.disabled = True
        else:
            self.previous_page.disabled = False
            self.begin_page.disabled = False
            
        if self.curr_page == self.page:
            self.next_page.disabled = True
            self.end_page.disabled = True
        else:
            self.next_page.disabled = False
            self.end_page.disabled = False
            
        await ctx.edit_original_response(embed=self.bans_page[self.curr_page] , view= self)
        
