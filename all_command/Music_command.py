from kuumuu_import import *

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

class Music():
    def __init__(self , client) -> None:
        self.__client__ = client
        
        self.__api_service_name__ = "youtube"
        self.__api_version__ = "v3"
        self.__client_secrets_file__ = "D:/data_base/client_secret_CLIENTID.json"
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        self.__client_secrets_file__, scopes)
    
        self.__credentials__ = flow.run_local_server()
        self.__ytb__ = googleapiclient.discovery.build(
            self.__api_service_name__, self.__api_version__, credentials=self.__credentials__)
        
        
        self.__ctrack__ = defaultdict(self.__def_music__)
        self.__ptrack__ = defaultdict(self.__def_music__)
        
        self.__isloop__ = defaultdict(self.__def_music_support__)
        
        self.__isdone__ = defaultdict(self.__def_music_support__)
        
        super().__init__()
    
    def __def_music__(num  : int):
        return deque([])
    
    def __def_music_support__(num : int):
        return None
    
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

    async def __add_to_queue__(self , ctx: discord.Interaction , url: str = None , query: str = None , list_url:str = None):
        embeb = discord.Embed(title="" , color= self.__client__.support.get_kuumo_color())
        
        if query != None:
            lists = []
        
            request = self.__ytb__.search().list(
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
                request1 = self.__ytb__.videos().list(
                            part="snippet,contentDetails,statistics",
                            id=j['id']['videoId']
                        )

                embeb1 = discord.Embed(title=f"Track's info" , color= self.__client__.support.get_kuumo_color())
                response1 = request1.execute()
                i = response1["items"][0]
                
                link = i['id']

                embeb1.set_thumbnail(url= i['snippet']['thumbnails']['default']['url'])

                embeb1.add_field(name="Track's Name: " , value= i['snippet']['title'] , inline= True)
                embeb1.add_field(name="Link:" , value=link , inline= True)
                embeb1.add_field(name="Channel: " , value=  i['snippet']['channelTitle'] , inline= False )

                embeb1.add_field(name="Viewers: " , value= i['statistics']['viewCount'] , inline= True)
                embeb1.add_field(name="Likers: " , value= i['statistics']['likeCount'] , inline= True)

                embeb1.add_field(name="Duration: " , value=await self.__change_time__(i['contentDetails']['duration']) , inline= True)
                
                lists.append(embeb1)
                if (cnt == 5):
                    break
                
            await ctx.followup.send(view= Search( ctx= ctx , client= self ,result= lists) )

            return
            
        elif url != None:
            self.__ctrack__[ctx.guild_id].append(url[len(url) - 11:])
            embeb1 = Embed(title=f"Track's info" , color= self.__client__.support.get_kuumo_color())
            embeb1.add_field(name="" , value=f"Track have been added to queue")
            await ctx.followup.send(embed= embeb1)
            self.__isdone__ = True
            return
        
        elif list_url != None:
            embeb1 = Embed(title=f"Track's info" , color= self.__client__.support.get_kuumo_color())

            URL = list_url[list_url.find('=') + 1 : ]
            
            request = self.__ytb__.playlistItems().list(
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
                        self.__ctrack__[ctx.guild_id].append(i['snippet']['resourceId']['videoId'])
                        cnt+=1
                        
                request = self.__ytb__.playlistItems().list(
                    part="snippet,contentDetails",
                    maxResults=100,
                    pageToken= temp,
                    playlistId= URL
                    )
                response = request.execute() 
                temp = response.get('nextPageToken', None)

            for i in response['items']:
                if i['snippet']['title'] != 'Deleted video' and i['snippet']['title'] != "Private video":
                    self.__ctrack__[ctx.guild_id].append(i['snippet']['resourceId']['videoId'])
                    cnt+=1
                        
            # embeb1.add_field(name="Warning: " , value=f"The feature is not currently activated. Please contact <@950354453033263175> or `mod` for assistance")
            embeb1.add_field(name="" , value=f"{cnt} tracks have been added to queue")
            
            await ctx.followup.send(embed= embeb1)
            self.__isdone__ = True
            return
        else:
            embeb.add_field(name="Warning:" , value=f'Please use youtube_url or query to search on youtube!')
            await ctx.channel.send(embed= embeb)
            self.__isdone__ = True 

            return
        
    async def __connecting__(self , ctx : discord.Interaction):
        voice_clientt : VoiceClient
        channel = ctx.user.voice.channel
        voice_clientt = discord.utils.get(self.__client__.voice_clients, guild=ctx.guild)
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
        voice_clientt = await self.__connecting__(ctx= ctx)
        
        if voice_clientt.is_playing():
            return
        
        curr_list = self.__ctrack__[id]
        pre_list = self.__ptrack__[id]
            
        while len(curr_list) != 0:

            if(voice_clientt.is_connected() == False):
                return
            
        

            url = curr_list[0]
            
            if url == None:
                curr_list.popleft()
                continue
            
            temp = "https://www.youtube.com/watch?v="+url
            
            # print(curr_list)
            # print(pre_list)
            # print(temp)
            
            song = pafy.new(url=temp)  # creates a new pafy object
            audio = song.getbestaudio()  # gets an audio source
            tempp = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
            
            while voice_clientt.is_playing() or voice_clientt.is_paused():
                await asyncio.sleep(1.0)   
                
            voice_clientt.play(tempp)
            
            embeb1 = Embed(title=f"Track's info" , color= self.__client__.support.get_kuumo_color())
            request = self.__ytb__.videos().list(
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
            embeb1.add_field(name="Duration: " , value=await self.__change_time__(i['contentDetails']['duration']) , inline= True)
            
            await ctx.channel.send(embed= embeb1)
            
            while voice_clientt.is_playing() or voice_clientt.is_paused():
                await asyncio.sleep(1.0)
            
            if len(curr_list)>0:
                if self.__isloop__[id] == False:
                    pre_list.append(curr_list[0])
                else:
                    curr_list.append(curr_list[0])
                curr_list.popleft()    
                
            curr_list = self.__ctrack__[id]  
        return
    
    async def ntrack(self , ctx : discord.Interaction , id:int):
        '''
            pramater:
                id : must be Member.id or Guild.id
        '''
        voice_clientt = await self.__connecting__(ctx= ctx)
    
        voice_clientt.stop()
            
        curr_list = self.__ctrack__[id]
        pre_list = self.__ptrack__[id]
        
        if self.__isloop__[id] == False:
            pre_list.append(curr_list[0])
        else:
            curr_list.append(curr_list[0])
        curr_list.popleft()   
        
        await ctx.response.send_message("Playing next track...")
        
        await self.play(ctx= ctx , id= id)
    
    async def ptrack(self , ctx : discord.Interaction , id:int):
        voice_clientt = await self.__connecting__(ctx= ctx)
    
        voice_clientt.stop()
            
            
        curr_list = self.__ctrack__[id]
        pre_list = self.__ptrack__[id]
        
        if self.__isloop__[id] == False:  
            curr_list.appendleft(pre_list[-1])
            pre_list.pop()
        else:
            curr_list.appendleft(curr_list[-1])
            curr_list.pop()   
            
        await ctx.response.send_message("Playing previous track...")
            
        await self.play(ctx= ctx , id= id)
        
    async def shuffle(self , ctx : discord.Interaction, id : int , mode : str):
        voice_clientt = await self.__connecting__(ctx= ctx)
        
        
        tracks = []
        
        curr_list = self.__ctrack__[id]
        pre_list = self.__ptrack__[id]
        
        if (mode == "False"):
            while(len(pre_list) > 0):
                tracks.append(pre_list[0])
                pre_list.popleft()
                
        while(len(curr_list)  > 1):
            tracks.append(curr_list[-1])
            curr_list.pop()
        
        shuffle(tracks)
        
        for i in tracks:
            self.__ctrack__[id].append(i)
            
        
        await self.play(ctx= ctx , id= id)
            
    
    async def stop(self , ctx: discord.Interaction , id : int):
        voice_clientt = await self.__connecting__(ctx= ctx)
        if (voice_clientt.is_playing()):
            voice_clientt.stop()
            
        while( len (self.__ctrack__[id]) > 0):
            self.__ctrack__[id].popleft()
            
        while( len (self.__ptrack__[id]) > 0):
            self.__ptrack__[id].popleft()
        
        return   
    
    async def pause(self , ctx: discord.Interaction):
        voice_clientt = await self.__connecting__(ctx= ctx) 
        if voice_clientt.is_playing():
            voice_clientt.pause()
        
        await ctx.response.send_message("Pausing...")
        
    async def setloop(self , ctx : discord.Interaction , loop):
        if loop.value == "True":
            self.__isloop__[ctx.guild_id] = True
        else:
            self.__isloop__[ctx.guild_id] = False
            
        await ctx.response.send_message(f'Your track has been change Loop to: {loop.value}')
        
    async def resume(self , ctx: discord.Interaction):
        voice_clientt = await self.__connecting__(ctx= ctx)
        if voice_clientt.is_paused():
            voice_clientt.resume()
        
        await ctx.response.send_message("Now playing...")
    
    async def join(self, ctx:discord.Interaction):
        channel = ctx.user.voice.channel
        await channel.connect()
        
        await ctx.response.send_message(f"I have been joined <#{channel.id}>")

    async def leave(self , ctx : discord.Interaction):
        channel = ctx.guild.voice_client
        await channel.disconnect()

        await ctx.response.send_message(f"I have been leaved")
        
    async def queue(self , ctx:discord.Interaction , id : int):
        
        await ctx.response.defer(thinking= True)
        lists = []
        
        for i in self.__ctrack__[id]:
            lists.append(i)
            
        tempp   = Show_queue(client= self , ctx= ctx , list= lists)
        
        
        await ctx.followup.send(view= tempp)
        
        await temp(self=tempp , ctx= ctx)

class Show_queue(View):
    def __init__(self, client : Music , ctx : discord.Interaction , list:list , timeout: float | None = 180):
        self.__client__ = client
        self.ctx = ctx
        self.done = False
        self.curr_page = 0  
        self.bans = list
        self.bans_numb = len(list)
        self.page = self.bans_numb // 10 -1  if self.bans_numb % 10 == 0 else self.bans_numb//10 
        self.bans_page = self.get_options()
        
        super().__init__(timeout=timeout)
        
    def get_track(self , url:str):
        
        
        temp = "https://www.youtube.com/watch?v="+url
        
        request = self.__client__.__ytb__.videos().list(
            part="snippet,contentDetails,statistics",
            id=url
        )
        response =  request.execute()
        i = response["items"][0]
                
        return i['snippet']['title']
        
    def get_options(self):
        lists = []
                
        i = 0
        while(i < self.bans_numb):
            embed = Embed(title="" , color= self.__client__.__client__.support.get_kuumo_color())
            if (i % 10 == 0):
                embed.add_field(name=" ", value=f'{i % 10 + 1 + 10*len(lists)}. {self.get_track(url= self.bans[i])}' , inline= True)
                i=i+1
                while(i % 10 != 0):
                    if i == self.bans_numb:
                        break
                    embed.add_field(name=" ", value=f'{i % 10 + 1 + 10*len(lists)}. {self.get_track(url= self.bans[i])}' , inline= True)
                    i=i+1
                
            lists.append(embed)
        
        return lists

    @button(label="<" , custom_id="2" , style= discord.ButtonStyle.blurple)
    async def previous_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = self.curr_page - 1

    @button(label=">" , custom_id="4" , style= discord.ButtonStyle.blurple)
    async def next_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = self.curr_page + 1
    
    @button(label="<<" , custom_id="1" , style= discord.ButtonStyle.blurple )
    async def begin_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = 0
        
    @button(label=">>" , custom_id="5" , style= discord.ButtonStyle.blurple )
    async def end_page(self , ctx : discord.Interaction , butt_oj = Button):
        self.curr_page = self.page
        
    @button(label="X" , custom_id="3" , style= discord.ButtonStyle.red)
    async def end(self , ctx : discord.Interaction, butt_oj = Button):
        self.done = True
        
    @select(placeholder="Choose track that you want to delete" , custom_id="input" , min_values=1 , max_values=1 ,options=[
                                                                                discord.SelectOption(label=str(i) , value= str(i))
                                                                                    for i in range(1 , 11)               
                                                                                        ])
    async def input(self , ctx : discord.Interaction , select):
        numb = int( select.values[0])
        numb = self.curr_page*10 + numb
        print("https://www.youtube.com/watch?v=" + self.__client__.__ctrack__[ctx.guild_id][numb-1])
        
        del self.__client__.__ctrack__[ctx.guild_id][numb-1]
        
        select.disabled = True
        self.done = True
    
async def temp(self : Show_queue, ctx : discord.Interaction):
        
    while(self.done == False):
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
    
    for child in self.children:
        if child.__dict__['_rendered_row'] != 1:
            temp = child.__dict__['_underlying']
            temp.disabled = True
            
    await ctx.edit_original_response(content=f"Done", view= self)
        
    self.stop()
    
class Search(discord.ui.View):
    def __init__(self , client , ctx : discord.Interaction, result : List):
        super().__init__(timeout=180)
        self.result = result
        self.music = client

        
    @discord.ui.select(placeholder='Select other page to see other track for selecting your track to play', min_values=1, max_values=1, 
                        options=[
                            discord.SelectOption(label='1', description='The first Video'  , value= 1),
                            discord.SelectOption(label='2', description='The second video' , value= 2),
                            discord.SelectOption(label='3', description='The Third video'  , value= 3),
                            discord.SelectOption(label='4', description='The 4th video'    , value= 4),
                            discord.SelectOption(label='5', description='The 5th video'    , value= 5),
                            ])
    async def select_callback(self, interaction : discord.Interaction , select): # the function called when the user is done selecting options
        await interaction.response.edit_message(embed= self.result[ ord(select.values[0]) - 49 ])
        
    @discord.ui.button(label="Track 1", custom_id= "1" ,  style=discord.ButtonStyle.primary)
    async def first_button_callback(self,  interaction : discord.Interaction , button : ui.Button):
        self.music.__ctrack__[interaction.guild_id].append(self.result[0].fields[1].value)
        self.music.__isdone__ = True
        await interaction.channel.send(embed=self.result[0])
        self.stop()
    
    @discord.ui.button(label="Track 2", custom_id= "2" ,  style=discord.ButtonStyle.primary)
    async def second_button_callback(self,  interaction : discord.Interaction , button):
        self.music.__ctrack__[interaction.guild_id].append(self.result[1].fields[1].value)
        self.music.__isdone__ = True
        await interaction.channel.send(embed=self.result[1])
        self.stop()
        
    @discord.ui.button(label="Track 3", custom_id= "3" ,  style=discord.ButtonStyle.primary)
    async def third_button_callback(self,  interaction : discord.Interaction , button):
        self.music.__ctrack__[interaction.guild_id].append(self.result[2].fields[1].value)
        self.music.__isdone__ = True
        await interaction.channel.send(embed=self.result[2])
        self.stop()

    @discord.ui.button(label="Track 4", custom_id= "4" ,  style=discord.ButtonStyle.primary)
    async def four_button_callback(self,  interaction : discord.Interaction , button):
        self.music.__ctrack__[interaction.guild_id].append(self.result[3].fields[1].value)
        await interaction.channel.send(embed=self.result[3])
        self.music.__isdone__ = True
        self.stop()
        
    @discord.ui.button(label="Track 5", custom_id= "5" ,  style=discord.ButtonStyle.primary)
    async def five_button_callback(self,  interaction : discord.Interaction , button):
        self.music.__ctrack__[interaction.guild_id].append(self.result[4].fields[1].value)
        await interaction.channel.send(embed=self.result[4])
        self.music.__isdone__ = True
        self.stop()
        
        