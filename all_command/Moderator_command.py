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
                await member.timeout( datetime. timedelta(seconds= numb))
            elif chara == "min" or chara.startswith('minute'):
                await member.timeout(datetime.timedelta(minutes= numb) ) 
            elif chara == "hou" or chara.startswith('hour'):
                await member.timeout( datetime.timedelta(hours= numb) ) 
            elif chara == "ds" or chara.startswith('day'):
                await member.timeout( datetime.timedelta(days= numb) ) 
            elif chara == "we" or chara.startswith('week'):
                await member.timeout( datetime.timedelta(weeks= numb) )
                
            # await ctx.response.send_message(embed= embed) 

        else:
            raise MissingPermissions()
            
    async def untimeout(self , ctx : discord.Interaction, member: discord.Member):
        if ctx.user.top_role > member.top_role and ctx.user.top_role != member.top_role:
            emmeb = discord.Embed(title='' , color= self.__client__.support.get_kuumo_color())
            emmeb.add_field(name='' , value=f'{member} has been untimeout by {ctx.user}')
            await ctx.response.send_message(embed=emmeb)
            await member.timeout(datetime.timedelta(seconds=0))
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
        if (member == ctx.user and ctx.permissions.change_nickname):
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
        
    
        
    async def bans(self , ctx: discord.Interaction):
        
        await ctx.response.defer(thinking=True)
        lmao = []
    
        async for i in ctx.guild.bans():
            lmao.append(i)
        
        tempp = ViewButton(client= self.__client__ , ctx= ctx , list= lmao )
        
        if len(lmao) <1:
            embeb = discord.Embed(title="" , color=self.__client__.support.get_kuumo_color())
            embeb.add_field(name="" , value=f"I can't find any banxed member in your server")
            
            await ctx.followup.send(embed= embeb)
            
            return
        
        await ctx.followup.send(view= tempp)
        await temp(self= tempp , ctx= ctx)

class ViewButton(View):
    def __init__(self, client : Moderator , ctx : discord.Interaction , list:list , timeout: float | None = 180):
        self.__client__ = client
        self.ctx = ctx
        self.done = False
        self.curr_page = 0
        self.bans = list
        self.bans_numb = len(list)
        self.page = self.bans_numb // 10 -1  if self.bans_numb % 10 == 0 else self.bans_numb//10 
        
        
        self.bans_page = self.get_options(self.ctx)
        
        super().__init__(timeout=timeout)
    def get_options(self , ctx : discord.Interaction):
        lists = []
                
        i = 0
        while(i < self.bans_numb):
            embed = Embed(title="" , color= self.__client__.support.get_kuumo_color())
            if (i % 10 == 0):
                embed.add_field(name=" ", value=f'{i % 10 + 1}. {self.bans[i].user}' , inline= False)
                i=i+1
                while(i % 10 != 0):
                    if i == self.bans_numb:
                        break
                    embed.add_field(name="" , value=f'{i % 10 + 1}. {self.bans[i].user}' , inline= False)
                    i=i+1
                
            lists.append(embed)
            
        if len(lists) == 0:
            embed = Embed(title="" , color= self.__client__.support.get_kuumo_color())
            embed.add_field(name="" , value="Your server doesn't have baned member now")
            lists.append(embed)
        
        return lists

    @button(label="<<" , custom_id="1" , style= discord.ButtonStyle.blurple )
    async def begin_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = 0
    
    @button(label="<" , custom_id="2" , style= discord.ButtonStyle.blurple)
    async def previous_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = self.curr_page - 1

    @button(label=">" , custom_id="4" , style= discord.ButtonStyle.blurple)
    async def next_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = self.curr_page + 1

    @button(label=">>" , custom_id="5" , style= discord.ButtonStyle.blurple )
    async def end_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = self.page
        
    @button(label="X" , custom_id="3" , style= discord.ButtonStyle.red)
    async def end(self , ctx : discord.Interaction, butt_oj = Button):
        
        self.done = True
        self.stop()
        
    @select(placeholder="Choose your choice" , custom_id="input" , min_values=1 , max_values=1 ,options=[
                                                                                discord.SelectOption(label=str(i) , value= str(i))
                                                                                    for i in range(1 , 11)               
                                                                                        ])
    async def input(self , ctx : discord.Interaction , select):
        
        numb = int( select.values[0])
        numb = self.curr_page*10 + numb
        
        if numb > len(self.bans):
            pass
        
        temp = self.bans[numb-1].user
        
        await ctx.guild.unban(temp)
            
        self.bans_numb = self.bans_numb - 1
        
        self.page = self.bans_numb // 10 -1  if self.bans_numb % 10 == 0 else self.bans_numb//10 
        
        if self.bans_numb == 0:
            self.page = 0
            
        self.bans_page = self.get_options(ctx= ctx)
        
        
    
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
            
        if self.curr_page > self.page:
            self.curr_page = self.page-1
            
        if self.page == 0:
            self.curr_page = 0
            
        await ctx.edit_original_response(embed=self.bans_page[self.curr_page] , view= self)
        
    for child in self.children:
        if child.__dict__['_rendered_row'] != 1:
            temp = child.__dict__['_underlying']
            temp.disabled = True
            
    await ctx.edit_original_response(content=f"Done", view= self)
        
    self.stop()
