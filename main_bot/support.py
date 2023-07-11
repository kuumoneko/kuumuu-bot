from collections import defaultdict
from random import *
import discord

def def_value():
    return "Not Present"

def check_tin_juan(a):
    if a == "tin juan ko":
        return True
    if a == "tin chuẩn không":
        return True
    if a == "tin chuẩn ko" :
        return True
    if a == "tin juan không"  :
        return True
    if a == "tin chuẩn k" :
        return True
    if a == "tin juan k":
        return True
    if a == "tin juan hong":
        return True
    if a == "tin chuẩn hong":
        return True
    if a == "tin juan hông":
        return True
    if a == "tin chuẩn hông":
        return True
    return False


def get_name_of_time():
    check_time = []
    check_time.append("sec")
    check_time.append("min")
    check_time.append("hou")
    check_time.append("ds")
    check_time.append("we")
    
    return check_time

def get_time():
    timee = defaultdict(def_value)
    timee["sec"] = "seconds"
    timee["min"] = "minutes"
    timee["hou"] = "hours"
    timee["ds"] = "days"
    timee["we"] = "weeks"
    
    return timee

kurru = defaultdict(def_value)
emoji_temp = defaultdict(def_value)

def get_emoji(mclient):

    for sv in mclient.guilds:
        emojii : discord.Emoji
        for emojii in sv.emojis:
            # print(emojii.name , ' ', emojii.id)
            emoji_temp[emojii.name] = emojii.id
            # print(emojii.id , ' ' , emojii.name)
            # print(f'<:{emojii.name}:{emoji_temp[emojii.name]}>')
        
def get_notifi():
    
    kuumo = open("kuumuu_data/notification.txt" , "r+")
    list_obj = kuumo.readlines()
    
    for it in list_obj:
        it = it[ : -1]
        # print(it , end= 'mói')
        if (len(it) < 1):
            continue
        
        # print(it)
        a , b = map(str , it.split(' '))
        kurru[a] = b
        
def get_color():
    file = 'kuumuu_data/kuumo_color.txt'
    kuumo = open(file , "r")
    
    temp = kuumo.readlines()
    kuumo.close()
    for it in temp:
        it = it[1 : -2]
        
    return temp
        
kuumo_color = get_color()
        
def get_kuumo_color(temp):
    mid = randrange(0 , len(kuumo_color)-1 , 1)
    kurumu = temp[mid]
    kurumu = kurumu[ 1: -1]
    
    return int( int(kurumu, 16))


def change_time(string: str):

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

