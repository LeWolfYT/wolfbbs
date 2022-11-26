import os
import threading as th
import time as t
import colorama as c
import keyboard as k
import pyfiglet as f
import requests as r

c.init()

def move(x, y):
    print(f"\033[{y};{x}H")

def waitloop():
    while True:
        move(0, os.get_terminal_size()[0])
        print("\r     ", end="")
        if k.is_pressed("x"):
            return True
        elif k.is_pressed("m"):
            return False

def customcol(color):
    return f"\033[38;5;{color}m"

def rgb(r,g,b):
    return f"\033[38;2;{r};{g};{b}m"

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def multiprint(*args):
    for val in args:
        print(val)

clear()

w,h = os.get_terminal_size()

title = "Main Menu"

logo = customcol(10) + """8   8  8                  8\"\"\"\"8   8\"\"\"\"8   8\"\"\"\"8 
8   8  8 eeeee e     eeee 8    8   8    8   8      
8e  8  8 8  88 8     8    8eeee8ee 8eeee8ee 8eeeee 
88  8  8 8   8 8e    8eee 88     8 88     8     88 
88  8  8 8   8 88    88   88     8 88     8 e   88 
88ee8ee8 8eee8 88eee 88   88eeeee8 88eeeee8 8eee88""" + customcol(231)

def makewin(displogo: bool = False, back: bool = False, clearall: bool = True):
    w = os.get_terminal_size()[0]
    if clearall:
        os.system("clear")
    else:
        move(0,0)
    if back:
        titletxt = customcol(208) + title + "-" * (w - len(title) - 12) + f"(\033[1mM\033[0m{customcol(208)}enu)(e\033[1mX\033[0m{customcol(208)}it)" + customcol(231)
    else:
        titletxt = customcol(208) + title + "-" * (w - len(title) - 6) + f"(e\033[1mX\033[0m{customcol(208)}it)" + customcol(231)
    if displogo:
        multiprint(titletxt, logo)
    else:
        multiprint(titletxt)

def clock(fg: f.Figlet):
    clp = True
    def cloop():
        while clp:
            makewin(False, True)
            print(fg.renderText(t.strftime("%c", t.localtime())))
            t.sleep(0.2)
    ct = th.Thread(target=cloop)
    ct.start()
    
    w = waitloop()
    clp = False
    return w

def weather(fg: f.Figlet):
    units = "imperial"
    
    ip = r.get("http://ipwho.is/").json()["ip"]
    
    data = r.post("http://71.112.157.244:8296", json={"mode": "weather", "ip": ip, "units": units})
    jsondt = data.json()
    description = jsondt["weather"][0]["description"]
    #make the first letter uppercase
    temp = round(jsondt["main"]["temp"], 1)
    description = description[0].upper() + description[1:]
    wind = jsondt["wind"]["speed"]
    
    makewin(False, True)
    print(fg.renderText(str(temp)+""+("F" if units == "imperial" else "C")))
    print(str(wind) + " " + ("mph" if units == "imperial" else "m/s") + " wind")
    print(description)
    
    return waitloop()

def bulletin(fg: f.Figlet):
    #get bulletin
    ip = r.get("http://ipwho.is/").json()["ip"]
    
    bt = r.post("http://71.112.157.244:8296", json={"mode": "bulletin", "ip": ip}).json()
    hd = bt["headline"]
    bd = bt["body"]
    sig = bt["signature"]
    
    makewin(False, True)
    
    print(fg.renderText(hd))
    for txt in bd:
        print(txt)
        
    print("\n"+sig)
    return waitloop()

def commands(fig):
    history = []
    while True:
        os.system("clear")
        w, h = os.get_terminal_size()
        move(0,h-2)
        print("_"*w)
        cmd = input("> ")
        move(0,h-3)
        cmd = cmd.lower()
        if cmd == "time":
            print(t.strftime("%-I:%m %p", t.localtime()))
        elif cmd == "date":
            print(t.strftime("", t.localtime()))
        elif cmd in ["exit", "x"]:
            return True
        elif cmd in ["back", "b", "menu", "m"]:
            return False
        else:
            print("Invalid command!")

def main():
    makewin(True)
    options = [f"\033[1mC\033[0m{customcol(231)}lock",
               f"\033[1mW\033[0m{customcol(231)}eather",
               f"\033[1mB\033[0m{customcol(231)}ulletin"]#,
               #f"C\033[1mo\033[0m{customcol(231)}mmands"]
    print()
    multiprint(*options)

fig = f.Figlet(font="LCD")

main()

while True:
    if k.is_pressed("c"):
        title = "Clock"
        if clock(fig):
            break
        else:
            main()
    elif k.is_pressed("w"):
        title = "Weather"
        if weather(fig):
            break
        else:
            main()
    elif k.is_pressed("b"):
        title = "Bulletin"
        if bulletin(fig):
            break
        else:
            main()
    #elif k.is_pressed("o"):
    #    title = "Commands"
    #    if commands(fig):
    #        break
    #    else:
    #        main()
    elif k.is_pressed("x"):
        break
clear()
c.deinit()
