from kuumuu_import import *


class Support():
    def __init__(self , client) -> None:
        self.__client__ = client
        
        self.kuumo_color= list([
            0xCD5C5C,0xFF6A6A,0xEE6363,0xCD5555,0x8B3A3A,0xB22222,0xFF3030,0xEE2C2C,0xCD2626,0x8B1A1A,0xA52A2A,0xFF4040,0xEE3B3B,
            0x8B2323,0xFF8C00,0xFF7F00,0xEE7600,0xCD6600,0xFF6347,0xEE5C42,0xFF4500,0xEE4000,0xFF0000,0xEE0000,0xDC143C,0xCD3333
        ])
        
        self.list_temp = list([
                        "tin juan ko"      ,
                        "tin chuẩn không"  ,
                        "tin chuẩn ko"     ,
                        "tin juan không"   ,
                        "tin chuẩn k"      ,
                        "tin juan k"       ,
                        "tin juan hong"    ,
                        "tin chuẩn hong"   ,
                        "tin juan hông"    ,
                        "tin chuẩn hông"   ,
                    ])   

        self.notification = defaultdict(self.def_value)
        self.emojii = defaultdict(self.def_value)
        
        
        super().__init__()


    def def_value(string):
        return "None"

    def check_tin_juan(self, a : str):

        for i in self.list_temp:
            if a.find(i) != -1:
                return True
        return False


    def get_emoji(self):

        for sv in self.__client__.guilds:
            emojii : discord.Emoji
            for emojii in sv.emojis:
                # print(emojii.name , ' ', emojii.id)
                self.emojii[emojii.name] = emojii.id
                # print(emojii.id , ' ' , emojii.name)
                # print(f'<:{emojii.name}:{emoji_temp[emojii.name]}>')
            
    def get_notifi(self):
        
        kuumo = open("D:\\kuumuu-bot\\data_base\\notifications.txt" , "r+")
        list_obj = kuumo.readlines()
        
        for it in list_obj:
            it = it[ : -1]
            if (len(it) < 1):
                continue
            
            a , b = map(str , it.split(' '))
                        
            self.notification[a] = b
            
    async def update_database(self):
        while True:
            kuumo = open("D:\\kuumuu-bot\\data_base\\notifications.txt" , "w+" , encoding="utf-8")
            
            for i in self.notification:
                tmep = f"{i} {self.notification[i]}\n"
                kuumo.write(tmep)
            
            await asyncio.sleep(0.1)
 
    def get_kuumo_color(self):
        mid = randrange(0 , len(self.kuumo_color)-1 , 1)
        kurumu = self.kuumo_color[mid]
        return kurumu


