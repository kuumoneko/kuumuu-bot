from kuumuu_import import *

class Music():
    def __init__(self , client) -> None:
        self.__client__ = client
        self.__ctrack__ = defaultdict(self.__def_music__)
        self.__ptrack__ = defaultdict(self.__def_music__)
        
        self.__isloop__ = defaultdict(self.__def_music__)
        
        self.__isdone__ = defaultdict(self.__def_music__)
        
        super().__init__()
    
    def __def_music__(num  : int):
        return Queue([] , maxsize= 1000)
    
    async def __change_time__(self , string : str):
        check_list = ["D" , "H" , "M" , "S"]
        res = ""
        for char in check_list:
            temp = string.find(char)
            strtemp = ""
            if temp == -1:
                continue
            if (temp != -1):
                strtemp = string[ (temp-3)  : (temp-len(string))   ]
                
            k = len(strtemp)-1
            while(ord(strtemp[k]) >= 48 and ord(strtemp[k]) <= 57 and k > 0 ):
                k-=1

            for i in range (60 , 96):
                strtemp = strtemp.strip(chr(i))
            for i in range(97 , 123):
                strtemp = strtemp.strip(chr(i))
                
            if k != 0:
                strtemp = strtemp[  len(strtemp) - k  :  ]
            
            if strtemp != "":
                if (char == "D"):
                    res += strtemp + " days "
                if (char == "H"):
                    res += strtemp + " hours "
                if (char == "M"):
                    res += strtemp + " minutes "
                if (char == "S"):
                    res += strtemp + " seconds "
        
        return res

    async def add_to_queue(self , ctx: discord.Interaction , url: str = None , query: str = None , list_url:str = None):
        embeb = discord.Embed(title="" , color= await self.get_color())
        
        if query != None:
            lists = []
        
            request = self.ytb.search().list(
                part="snippet",
                maxResults=10,
                q= query
            )
            cnt =0

            response = request.execute()

            for j in response["items"]:

                if j['id']['kind'] != 'youtube#video':
                    continue

                cnt+=1
                request1 = self.ytb.videos().list(
                            part="snippet,contentDetails,statistics",
                            id=j['id']['videoId']
                        )

                embeb1 = discord.Embed(title=f"Track's info" , color= await self.get_color())
                response1 = request1.execute()
                i = response1["items"][0]
                
                link = i['id']

                embeb1.set_thumbnail(url= i['snippet']['thumbnails']['default']['url'])

                embeb1.add_field(name="Track's Name: " , value= i['snippet']['title'] , inline= True)
                embeb1.add_field(name="Link:" , value=link , inline= True)
                embeb1.add_field(name="Channel: " , value=  i['snippet']['channelTitle'] , inline= False )

                embeb1.add_field(name="Viewers: " , value= i['statistics']['viewCount'] , inline= True)
                embeb1.add_field(name="Likers: " , value= i['statistics']['likeCount'] , inline= True)

                embeb1.add_field(name="Duration: " , value=await self.change_time(i['contentDetails']['duration']) , inline= True)
                
                lists.append(embeb1)
                if (cnt == 5):
                    break
                
            await ctx.channel.send(view= Search( ctx= ctx , client= self ,result= lists) )

            
            
            return
            
        elif url != None:
            self.ctrack[ctx.guild_id].append(url[len(url) - 11:])
            embeb1 = Embed(title=f"Track's info" , color=await self.get_color())
            embeb1.add_field(name="" , value=f"Track have been added to queue")
            await ctx.followup.send(embed= embeb1)
            self.__isdone__ = True
            return
        
        elif list_url != None:
            embeb1 = Embed(title=f"Track's info" , color=await self.get_color())

            URL = list_url[list_url.find('=') + 1 : ]
            
            request = self.ytb.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=100,
                playlistId= URL
            )
            response = request.execute()
            
            temp = response.get('nextPageToken' , None)
            cnt=0

            while(temp != None):
                for i in response['items']:
                    if i['snippet']['title'] != 'Deleted video' and i['snippet']['title'] != "Private video":
                        self.ctrack[ctx.guild_id].append(i['snippet']['resourceId']['videoId'])
                        cnt+=1
                        
                request = self.ytb.playlistItems().list(
                    part="snippet,contentDetails",
                    maxResults=100,
                    pageToken= temp,
                    playlistId= URL
                    )
                response = request.execute() 
                temp = response.get('nextPageToken', None)

            for i in response['items']:
                if i['snippet']['title'] != 'Deleted video' and i['snippet']['title'] != "Private video":
                    self.ctrack[ctx.guild_id].append(i['snippet']['resourceId']['videoId'])
                    cnt+=1
                        
            # embeb1.add_field(name="Warning: " , value=f"The feature is not currently activated. Please contact <@950354453033263175> or `mod` for assistance")
            embeb1.add_field(name="" , value=f"{cnt} tracks have been added to queue")
            
            await ctx.followup.send(embed= embeb1)
            self.__isdone__ = True
            return
        else:
            embeb.add_field(name="Warning:" , value=f'Please use youtube_url or query to search on youtube!')
            await ctx.channel.send(embed= embeb)
            return
        
    async def connecting(self , ctx : discord.Interaction):
        voice_clientt : VoiceClient
        channel = ctx.user.voice.channel
        voice_clientt = discord.utils.get(self.voice_clients, guild=ctx.guild)
        if not voice_clientt is None:
            if not voice_clientt.is_connected():
                voice_clientt = await channel.connect()
        else:
            voice_clientt = await channel.connect() 
        return voice_clientt

    async def play(self , ctx : discord.Interaction , id:int):
        '''
            pramater:
                id : should be Member.id or Guild.id
        '''
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        voice_clientt = await self.connecting(ctx= ctx)
        
        if voice_clientt.is_playing():
            return
        
        curr_list = self.ctrack[id]
        pre_list = self.ptrack[id]
            
        while len(curr_list) != 0:

            if(voice_clientt.is_connected() == False):
                return

            url = curr_list[0]
            
            # print(curr_list)
            # print(pre_list)
            
            temp = "https://www.youtube.com/watch?v="+url
            
            song = pafy.new(url=temp)  # creates a new pafy object
            audio = song.getbestaudio()  # gets an audio source
            tempp = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
            
            
            
            while voice_clientt.is_playing() or voice_clientt.is_paused():
                await asyncio.sleep(1.0)   
                
            voice_clientt.play(tempp)
            
            embeb1 = Embed(title=f"Track's info" , color=await self.get_color())
            request = self.ytb.videos().list(
                part="snippet,contentDetails,statistics",
                id=url
            )
            response =  request.execute()
            i = response["items"][0]
            
            embeb1.set_thumbnail(url= i['snippet']['thumbnails']['default']['url'])

            embeb1.add_field(name="Track's Name: " , value= i['snippet']['title'] , inline= True)
            embeb1.add_field(name="Channel: " , value=  i['snippet']['channelTitle'] , inline= False )

            embeb1.add_field(name="Viewers: " , value= i['statistics']['viewCount'] , inline= True)
            embeb1.add_field(name="Likers: " , value= i['statistics']['likeCount'] , inline= True)

            embeb1.add_field(name="Duration: " , value=await self.change_time(i['contentDetails']['duration']) , inline= True)
            
            await ctx.channel.send(embed= embeb1)
            
            await asyncio.sleep(3.0)
            while voice_clientt.is_playing() or voice_clientt.is_paused():
                await asyncio.sleep(1.0)
            
            if len(curr_list)>0:
                if self.is_loop[id] == False:
                    pre_list.append(curr_list[0])
                else:
                    curr_list.append(curr_list[0])
                curr_list.popleft()    
                
            curr_list = self.ctrack[id]   
        return
    
    async def next_track(self , ctx : discord.Interaction , id:int):
        '''
            pramater:
                id : must be Member.id or Guild.id
        '''
        voice_clientt = await self.connecting(ctx= ctx)
    
        voice_clientt.stop()
            
        curr_list = self.ctrack[id]
        pre_list = self.ptrack[id]
        
        if self.is_loop[id] == False:
            pre_list.append(curr_list[0])
        else:
            curr_list.append(curr_list[0])
        curr_list.popleft()   
        
        await self.play(ctx= ctx , id= id)
    
    async def previous_track(self , ctx : discord.Interaction , id:int):
        voice_clientt = await self.connecting(ctx= ctx)
    
        voice_clientt.stop()
            
            
        curr_list = self.ctrack[id]
        pre_list = self.ptrack[id]
        
        if self.is_loop[id] == False:  
            curr_list.appendleft(pre_list[-1])
            pre_list.pop()
        else:
            curr_list.appendleft(curr_list[-1])
            curr_list.pop()   
            
        await self.play(ctx= ctx , id= id)
            
    
    async def stop_music(self , ctx: discord.Interaction , id : int):
        voice_clientt = await self.connecting(ctx= ctx)
        if (voice_clientt.is_playing()):
            voice_clientt.stop()
            
        while( len (self.ctrack[id]) > 0):
            self.ctrack[id].popleft()
            
        while( len (self.ptrack[id]) > 0):
            self.ptrack[id].popleft()
        
        return   
    
    async def pause_music(self , ctx: discord.Interaction):
        voice_clientt = await self.connecting(ctx= ctx) 
        if voice_clientt.is_playing():
            voice_clientt.pause()

        
    async def resume_music(self , ctx: discord.Interaction):
        voice_clientt = await self.connecting(ctx= ctx)
        if voice_clientt.is_paused():
            voice_clientt.resume()
    
    async def join(self, ctx:discord.Interaction):
        channel = ctx.user.voice.channel
        await channel.connect()

    async def leave(self , ctx : discord.Interaction):
        channel = ctx.guild.voice_client
        await channel.disconnect()



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
    def __init__(self , client , ctx : discord.Interaction, result : List):
        super().__init__(timeout=180)
        self.result = result
        self.music = client
        
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
        self.music.ctrack[interaction.guild].append(self.result[0].fields[1].value)
        await interaction.followup.send(embed=self.result[0])
        self.stop()
    
    @discord.ui.button(label="Track 2", custom_id= "2" ,  style=discord.ButtonStyle.primary)
    async def second_button_callback(self,  interaction : discord.Interaction , button):
        self.music.ctrack[interaction.guild].append(self.result[1].fields[1].value)
        await interaction.followup.send(embed=self.result[1])
        self.stop()
        
    @discord.ui.button(label="Track 3", custom_id= "3" ,  style=discord.ButtonStyle.primary)
    async def third_button_callback(self,  interaction : discord.Interaction , button):
        self.music.ctrack[interaction.guild].append(self.result[2].fields[1].value)
        await interaction.followup.send(embed=self.result[2])
        self.stop()

    @discord.ui.button(label="Track 4", custom_id= "4" ,  style=discord.ButtonStyle.primary)
    async def four_button_callback(self,  interaction : discord.Interaction , button):
        self.music.ctrack[interaction.guild].append(self.result[3].fields[1].value)
        await interaction.followup.send(embed=self.result[3])
        self.stop()
        
    @discord.ui.button(label="Track 5", custom_id= "5" ,  style=discord.ButtonStyle.primary)
    async def five_button_callback(self,  interaction : discord.Interaction , button):
        self.music.ctrack[interaction.guild].append(self.result[4].fields[1].value)
        await interaction.followup.send(embed=self.result[4])
        self.stop()