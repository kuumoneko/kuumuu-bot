from EdgeGPT.EdgeGPT import Chatbot , ConversationStyle
import json

import asyncio


cookies = json.loads(open("D:\\data_base\\cookies.json", encoding="utf-8").read())
edgechatbot = Chatbot(cookies=cookies)



message = "can you recommend me a PC config for programming, running server and machine learning"



async def moi():
    res = await edgechatbot.ask(prompt= message , conversation_style=ConversationStyle.creative , simplify_response= True)

    
    print(res['text'])
    
    
    print(res['sources_text'].replace("[" , "\n["))

    # print(json.dumps(res))



if __name__ == "__main__":
    
    asyncio.run(moi())