# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors

# import isodate
# import isoduration
# import datetime
# import os
# import pandas
# import asyncio
# import json


# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# __api_service_name__ = "youtube"
# __api_version__ = "v3"
# __client_secrets_file__ = "D:/data_base/client_secret_CLIENTID.json"
# flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
# __client_secrets_file__, scopes)
# __credentials__ = flow.run_local_server()
# __ytb__ = googleapiclient.discovery.build(
#     __api_service_name__, __api_version__, credentials=__credentials__)



# async def moi():

#     request = __ytb__.videos().list(
#                     part="snippet,contentDetails,statistics",
#                     id="mivcDoTjpQE"
#                 )
#     response =  request.execute()
#     video = response["items"][0]



#     print(json.dumps(video))
#     # return

#     # return
#     kuumo = video['contentDetails']['duration']

#     start = datetime.datetime.now().replace(microsecond=0)
#     end = datetime.datetime.now() + isoduration.parse_duration(kuumo)
#     end = end.replace(microsecond=0)
#     duration = end - start

#     print(start)
#     print(end)
#     print(end - start)



#     curr = datetime.timedelta(hours= 0 , minutes= 0  ,seconds=0)

#     while(curr < duration):
#         print(curr , '           ' , duration)
#         curr = curr + datetime.timedelta(seconds=1)
#         await asyncio.sleep(1)
    
# if __name__ == "__main__":
#     asyncio.run(moi())


import discord


embeb = discord.Embed(title="" , color=0xFF0000)

for i in range(1 , 11):

    embeb.add_field(name= str(i) , value=str(i))
    

embeb.remove_field(-1)

for i in embeb.fields:
    print(i.name , ' ' , i.value)
    
    
    
# embeb.

# embeb.add_field(na)