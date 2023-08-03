from kuumuu_import import *

class AI():
    def __init__(self , client) -> None:
        self.__client__ = client
        self.__chatting__ = AI_chat(ai= self)
        super().__init__()
        
    async def chat(self , ctx : discord.Interaction , message: str , isprivate : str , chatbot :str):
        
        if ctx.user == self.__client__.user:
            return
        username = str(ctx.user)
        self.__chatting__.current_channel = ctx.channel
        logger.info(
            f"\x1b[31m{username}\x1b[0m : /chat [{message}] [Private = {isprivate}] [Chat Bot = {chatbot}]  in ({self.__chatting__.current_channel})")

        await self.__chatting__.enqueue_message(ctx, message  , chatbot , isprivate)
        
        
class AI_chat():
    def __init__(self , ai) -> None:
        self.ai = ai

        self.current_channel = None
        self.cookies = json.loads(open("D:\\data_base\\cookies.json", encoding="utf-8").read())
        
        self.edgechatbot = EdgeChatbot(cookies=self.cookies)
        
        self.Secure_1PSID = self.ai.__client__.Secure_1PSID

        self.Secure_1PSIDTS = self.ai.__client__.Secure_1PSIDTS
        
        self.bardchatbot =  BardChatBot(self.Secure_1PSID, self.Secure_1PSIDTS)
        
        self.message_queue = asyncio.Queue()
        
        
        super().__init__()
        
    async def process_messages(self):
        while True:
            if self.current_channel is not None:
                while not self.message_queue.empty():
                    async with self.current_channel.typing():
                        message, user_message , chatbot , isPrivate = await self.message_queue.get()
                        try:
                            await self.send_message(message, user_message , chatbot , isPrivate)
                        except Exception as e:
                            logger.exception(
                                f"Error while processing message: {e}")
                        finally:
                            self.message_queue.task_done()
            await asyncio.sleep(0.1)
    
    async def enqueue_message(self, message, user_message , chatbot , isPrivate):
        
        await message.response.defer(ephemeral= True if isPrivate == "True" else False )
        self.ctx = message
        await self.message_queue.put((message, user_message , chatbot , isPrivate))

    async def send_message(self, message, user_message , chatbot , isPrivate):
        author = message.user.id
        message = self.ctx
        
        try:
            response = (f'> **{user_message}** - <@{str(author)}> \n\n')
            
            if chatbot == "Bard":
                response = f"{response}{await responses.bard_handle_response(user_message, self)}"
            elif chatbot == "Bing Balanced":
                response = f"{response}{await responses.bing_handle_response(message=user_message, kclient=self , conversation_style=ConversationStyle.balanced)}"
            elif chatbot == "Bing Precise":
                response = f"{response}{await responses.bing_handle_response(message=user_message, kclient=self , conversation_style=ConversationStyle.precise)}"
            elif chatbot == "Bing Creative":
                response = f"{response}{await responses.bing_handle_response(message=user_message, kclient=self , conversation_style=ConversationStyle.creative)}"
                
            '''
            value="Bing Creative"),
            app_commands.Choice(name="Bing AI Balanced" , value="Bing Balanced"),
            app_commands.Choice(name="Bing AI Precise" , value="Bing Precise"),
            app_commands.Choice(name="Google Bard" , value="Bard")
            '''
            
            
            while response.find("[^") != -1:
                remp = response.find("[^")
                temp = response[  remp     : (len(response) + 5 + remp) - len(response)  ]
                response=  response.replace(temp , "")
                
                
            print(len(response))
            print((response))
            
            char_limit = 1900
            res_lenght = 0
            res_mess = []
            i = 0
            res = ""
            
            if len(response) > char_limit:
                temp = response.split('\n')
                lenght = len(temp)
                
                while i < lenght-1:
                    if temp[i].find('[') == -1 and temp[i].find(']') == -1:
                    
                        if len(res + temp[i]) < char_limit:
                            res = res + temp[i] + '\n'
                        else:
                            res_mess.append(res)
                            res = temp[i] + '\n'
                    i=i+1

                res_mess.append(res)
                for mess in res_mess:
                    await message.followup.send(mess , ephemeral= True if isPrivate == "True" else False)
            else:
                await message.followup.send(response , ephemeral= True if isPrivate == "True" else False)
        except Exception as e:
            await message.followup.send(f"> **ERROR: Something went wrong, please try again later!** \n ```ERROR MESSAGE: {e}```" , ephemeral= True if isPrivate == "True" else False)

            logger.exception(f"Error while sending message: {e}")

