from src import personas
from src.log import logger
from asgiref.sync import sync_to_async
from EdgeGPT.EdgeGPT import ConversationStyle
import json

async def official_handle_response(message, kclient) -> str:
    return await sync_to_async(kclient.chatbot.ask)(message)

async def unofficial_handle_response(message, kclient) -> str:
    async for response in kclient.chatbot.ask(message):
        responseMessage = response["message"]
    return responseMessage

async def bard_handle_response(message, kclient) -> str:
    response = await sync_to_async(kclient.bardchatbot.ask)(message)
    responseMessage = response["content"]
    return responseMessage

async def bing_handle_response(message, kclient, conversation_style = ConversationStyle) -> str:
    try:
        response = await kclient.edgechatbot.ask(prompt = message,
                                            conversation_style = conversation_style,
                                            simplify_response = True)
        # async for i in response:
        #     print(i)
        # print(json.loads(json.dumps(response)))
        responseMessage = response['text']
    except Exception as e:
        logger.error(f'Error occurred: {e}')
        await kclient.edgechatbot.reset()
        raise Exception("Bing is fail to continue the conversation, this conversation will automatically reset.")

    return responseMessage


# prompt engineering
async def switch_persona(persona, kclient) -> None:
    if kclient.chat_model ==  "UNOFFICIAL":
        kclient.chatbot.reset_chat()
        async for _ in kclient.chatbot.ask(personas.PERSONAS.get(persona)):
            pass
    elif kclient.chat_model == "OFFICIAL":
        kclient.chatbot = kclient.get_chatbot_model(prompt=personas.PERSONAS.get(persona))
    elif kclient.chat_model == "Bard":
        kclient.chatbot = kclient.get_chatbot_model()
        await sync_to_async(kclient.chatbot.ask)(personas.PERSONAS.get(persona))
    elif kclient.chat_model == "Bing":
        await kclient.chatbot.reset()
        async for _ in kclient.chatbot.ask_stream(personas.PERSONAS.get(persona)):
            pass
