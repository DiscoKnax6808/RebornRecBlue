import os
import requests
import random
from colors import *
import server
import winsound
import time

version = 1.0
isfirsttime = False



BASE_DIR = os.path.join(os.getcwd(), "SaveData")

isfirsttime=not os.path.isdir(BASE_DIR)

def clear():
    print("\033[H\033[J")

clear()

def downloaddata(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"FAILED TO RESOLVE DOWNLOAD: {url}")


def downloadbytes(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"FAILED TO RESOLVE DOWNLOAD: {url}")


def termname(title):
    os.system(f"title {title}")

def mainmenu():
    clear()

    termname("Reborn Rec Blue Main Menu")


    print(f"{CBlue}Reborn Rec Blue - Old RecRoom Server Software. (Version: Public Release: {str(version)})")
    print()
    print("Discord Server: https://discord.gg/Nq3hDeZgh9") 
    print("Click on this link to view a list of tested builds: https://shorturl.at/PxTBb")
    print("Made By @nullmason on discord")
    print()
    print("(1) What's New")
    print("(2) Settings Menu")
    print("(3) Modify Local Profile")
    print("(4) Build Download Link")
    print("(5) Start Server")
    print()
    winsound.Beep(700, 100)

    selection = input("")

    if selection == "1":
        clear()
        print(downloaddata("https://raw.githubusercontent.com/DiscoKnax6808/RebornRecBlue/refs/heads/main/datatodownload/changelog.txt"))
        print()
        print("Press enter to go back to main menu")
        input()
        mainmenu()
    elif selection == "2":
        mainmenu()
    elif selection == "3":
        mainmenu()
    elif selection == "4":
        mainmenu()
    elif selection == "5":
        clear()
        termname("Waiting for Build.....")
        winsound.Beep(700, 100)
        os.system("py server.py")
        quit()
    else:
        print()
        print("You didnt enter a valid option.")
        input()
        quit()



def RUN():
    if isfirsttime:
        clear()
        termname("Reborn Rec Blue Intro")
        print(CBlue + f"Welcome to Reborn Rec Blue {str(version)}")
        print("Is this your first time using RebornRec Blue?")
        print()
        text1 = input("Yes or No (Y,N) : " + CReset)

        if text1.lower() == "y":
            termname("Reborn Rec Blue Tutorial")
            clear()
            print(CBlue + "In that case, welcome to Reborn Rec Blue!")
            print("RebornRec Blue is a Python FastAPI Port of the Reborn Rec Client made by Aqquad\n")
            print("Reborn Rec Blue is server software that emulates the servers of previous RecRoom Versions")
            print()
            print("To use Reborn Rec Blue, You'll need to have builds as well!")
            print("To download builds, go to https://rebornrec.bluerift.lol/build_downloads to download a build.")
            print()
            input("Press Enter to Continue. : " +CReset)

            clear()
            print(CBlue + "Now that you have a build, what you're going to do is as follows:")
            print()
            print("  - Unzip the build using an Unarchiver.")
            print("  - Start the server by pressing 5 on the main menu.")
            print("  - Run Recroom_Release.exe/RecRoom.exe from the folder of the build you downloaded.")
            print()
            print("And that's it! Press Enter to go to the main menu, where you will be able to start the server!" + CReset)

            input()

            mainmenu()





        elif text1.lower() == "n":
            mainmenu()

    else:
        mainmenu()


def SETUP():
    folders = [
        os.path.join(BASE_DIR, "App"),
        os.path.join(BASE_DIR, "Photos"),
        os.path.join(BASE_DIR, "Profile"),
        os.path.join(BASE_DIR, "Rooms"),
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)


    print(CGreen+ "Setting up... (May take a minute to download everything.)" + CReset)
    winsound.Beep(700, 100)
    with open(f"{BASE_DIR}\\avatar.txt", "w", encoding="utf-8") as f:
        f.write(downloaddata("https://raw.githubusercontent.com/DiscoKnax6808/RebornRecBlue/refs/heads/main/datatodownload/avatar.txt"))
    with open(f"{BASE_DIR}\\avataritems.txt", "w", encoding="utf-8") as f:
        f.write(downloaddata("https://raw.githubusercontent.com/DiscoKnax6808/RebornRecBlue/refs/heads/main/datatodownload/avataritems.txt"))
    with open(f"{BASE_DIR}\\equipment.txt", "w", encoding="utf-8") as f:
        f.write(downloaddata("https://raw.githubusercontent.com/aqquad/RebornRec/main/equipment.txt"))
    with open(f"{BASE_DIR}\\consumables.txt", "w", encoding="utf-8") as f:
        f.write(downloaddata("https://raw.githubusercontent.com/aqquad/RebornRec/main/consumables.txt"))
    with open(f"{BASE_DIR}\\gameconfigs.txt", "w", encoding="utf-8") as f:
        f.write(downloaddata("https://raw.githubusercontent.com/aqquad/RebornRec/main/gameconfigs.txt"))
    with open(f"{BASE_DIR}\\baserooms.txt", "w", encoding="utf-8") as f:
        f.write(downloaddata("https://raw.githubusercontent.com/aqquad/RebornRec/main/baserooms.txt"))
    with open(f"{BASE_DIR}\\profileimage.png", "wb") as f:
        f.write(downloadbytes("https://raw.githubusercontent.com/DiscoKnax6808/RebornRecBlue/refs/heads/main/rebornrecblue.png"))
    with open(f"{BASE_DIR}\\privaterooms.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open(f"{BASE_DIR}\\Profile\\userid.txt", "w", encoding="utf-8") as f:
        f.write(str(random.randint(1000000, 10000000)))
    with open(f"{BASE_DIR}\\Profile\\userid.txt", "r", encoding="utf-8") as f:
        userid = int(f.read())
        with open(f"{BASE_DIR}\\Profile\\username.txt", "w", encoding="utf-8") as a:
            a.write(f"BlueRebornRec User #{userid}")

    with open(f"{BASE_DIR}\\Profile\\cheer.txt", "w", encoding="utf-8") as f:
        f.write(str(random.randint(1,6))+"0")

    with open(f"{BASE_DIR}\\Profile\\level.txt", "w", encoding="utf-8") as f:
        f.write(str(random.randint(10,51))+"0")

    with open(f"{BASE_DIR}\\settings.txt", "w", encoding="utf-8") as f:
        f.write(downloaddata("https://raw.githubusercontent.com/DiscoKnax6808/RebornRecBlue/refs/heads/main/datatodownload/settings.txt"))

    with open(f"{BASE_DIR}\\outfits.txt", "w", encoding="utf-8") as f:
        f.write("[]")

    with open(f"{BASE_DIR}\\configv2.txt", "w", encoding="utf-8") as f:
        f.write(downloaddata("https://raw.githubusercontent.com/DiscoKnax6808/RebornRecBlue/refs/heads/main/datatodownload/configv2.txt"))
    with open(f"{BASE_DIR}\\gamesession.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open(f"{BASE_DIR}\\discord.png", "wb") as f:
        f.write(downloadbytes("https://github.com/DiscoKnax6808/RebornRecBlue/blob/main/datatodownload/discord.png?raw=true"))


        


    
    




if not os.path.isdir(BASE_DIR):
    SETUP()



RUN()
