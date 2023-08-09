import datetime
import pkg_resources
from subprocess import call
import setuptools


def update():
    kuumo = open("D:\\data_base\\update_requirements.txt"  , "r" , encoding="utf-8")


    inputt = kuumo.readlines()
    kuumo.close()
    year = inputt[0][:-1]
    month = inputt[1][:-1]
    day = inputt[2][:-1]
    hour = inputt[3][:-1]
    minute = inputt[4][:-1]
    second = inputt[5]
    noww = datetime.datetime.now().replace(microsecond=0)
    latest_update = datetime.datetime(year=int(year) , month=int(month) , day= int(day) , hour=int(hour) , minute=int(minute) , second=int(second))
    print(f"Now: {noww}")
    print(f"Latest update: {latest_update}")



    if noww - latest_update > datetime.timedelta(days=1):
        call("pip list --outdated > D:\data_base\outdated.txt" , shell= True)
        
        call("pip install -U wheel" , shell=True)
        
        call("pip install -U pip" , shell=True)
        
        
        
        with open("D:\data_base\outdated.txt",'r') as packages_file:
        #these two readline() for first 2 rows
            packages_file.readline()
            packages_file.readline()

            package= True

            while package:
                package= packages_file.readline()
                if package.split():
                    package_name =package.split()[0]
                    print("Update-->",package_name)
                    call(f"pip install -U {package_name} " , shell=True)
                    
        kuumo = open("D:\\data_base\\update_requirements.txt"  , "w" , encoding="utf-8")
        
        kuumo.write(f"{noww.year}\n")
        kuumo.write(f"{noww.month}\n")
        kuumo.write(f"{noww.day}\n")
        kuumo.write(f"{noww.hour}\n")
        kuumo.write(f"{noww.minute}\n")
        kuumo.write(f"{noww.second}\n")
