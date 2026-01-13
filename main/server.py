import uvicorn, asyncio, os, shutil, json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from colors import *
import time
import random
import math
import aiohttp
from pathlib import Path

active_ws: WebSocket | None = None
discord_ws: aiohttp.ClientWebSocketResponse | None = None
discord_http: aiohttp.ClientSession | None = None

clients = {}
PRESENCE_FILE = Path("SaveData/gamesession.txt")

build_date = "2016"


BASE_DIR = os.path.join(os.getcwd(), "SaveData")

def read_int_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return int(f.read())
    except:
        return 0  

def read_str_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "UNKNOWN"  

def read_json_file(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[JSON LOAD ERROR] {path} -> {e}")
        return default 

userid = read_int_file(f"{BASE_DIR}\\Profile\\userid.txt")
username = read_str_file(f"{BASE_DIR}\\Profile\\username.txt")
selectedCheer = read_int_file(f"{BASE_DIR}\\Profile\\cheer.txt")
level = read_int_file(f"{BASE_DIR}\\Profile\\level.txt")
configs = read_json_file(f"{BASE_DIR}\\configv2.txt")
configsall = read_json_file(f"{BASE_DIR}\\gameconfigs.txt")
avatar = read_json_file(f"{BASE_DIR}\\avatar.txt")
settings = read_json_file(f"{BASE_DIR}\\settings.txt")
avataritems = read_json_file(f"{BASE_DIR}\\avataritems.txt")
equipment = read_json_file(f"{BASE_DIR}\\equipment.txt")
consumables = read_json_file(f"{BASE_DIR}\\consumables.txt")
rooms = read_json_file(f"{BASE_DIR}\\Rooms\\rooms.json")

app = FastAPI()
wsserver = FastAPI()
img = FastAPI()

wsserver.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def nameserver():
    return {"API": "https://localhost:2001", "Images": "http://localhost:2004", "Notifications": "ws://localhost:2002"}

@app.get("/http")
async def nameserver():
    return {"API": "http://localhost:2003", "Images": "http://localhost:2004", "Notifications": "ws://localhost:2002"}

@app.get("/httpSR")
async def nameserver():
    return {"API": "http://localhost:2003", "Images": "http://localhost:2004", "Notifications": "http://localhost:2003"}

years = ["2016","2017","2018","2019","2020","2021","2022", "2023"]

@app.get("/api/versioncheck/v3")
@app.get("/api/versioncheck/v2")
@app.get("/api/versioncheck/v1")
async def versioncheckv1(request: Request):

    v = request.query_params("v")

    vyear = v[0]+v[1]+v[2]+v[3]

    if vyear in years:
        build_date = vyear

    return {"ValidVersion": True}

@app.post("/api/players/v1/getorcreate")
async def v1getorcreate(request: Request):
    return {
        "Id": userid,
        "Username": username,
        "DisplayName": username,
        "XP": 67,
        "Level": level,
        "Reputation": 0,
        "Verified": True,
        "Developer": True,
        "HasEmail": True,
        "CanReceiveInvites": True,
        "ProfileImageName": "profileimage.png",
        "HasBirthday": True,
        "PhoneLastFour": "RebornRecBlue",
        "EmailEnteredAt": "2025-12-15 17:12:09",
        "PlayerReputation": {
            "Noteriety":0,"CheerGeneral":0,"CheerHelpful":0,"CheerGreatHost":0,
            "CheerSportsman":0,"CheerCreative":0,"CheerCredit":77,
            "SubscriberCount":2,"SubscribedCount":0,"SelectedCheer":int(selectedCheer)
        },
        "PlatformIds":{
            "Platform":0,
            "PlatformId":1
        }
    }



@app.post("/api/platformlogin/v1/logincached")
async def platformloginv1():
    return {
        "Error":"",
        "AnalyticsSessionId":0,
        "CanUseScreenMode":True,
        "Token": "67 Mangoes",
        "PlayerId":userid,
        "Error":"",
        "FirstLoginOfTheDay":True,
        "Player":{
        "Id": userid,
            "Username": username,
            "DisplayName": username,
            "RegistrationStatus": 2,
            "JuniorProfile": False,
            "PendingJunior": False,
            "ForceJuniorImages": False,
            "AvoidJuniors": True,
            "HasBirthday": True,
            "XP": 67,
            "Level": 99,
            "Reputation": 0,
            "Verified": True,
            "Developer": True,
            "HasEmail": True,
            "CanReceiveInvites": True,
            "ProfileImageName": "profileimage.png",
            "PhoneLastFour": "RebornRecBlue",
            "EmailEnteredAt": "2025-12-15 17:12:09",
            "PlayerReputation": {
                "Noteriety": 0,
                "CheerGeneral": 0,
                "CheerHelpful": 0,
                "CheerGreatHost": 0,
                "CheerSportsman": 0,
                "CheerCreative": 0,
                "CheerCredit": 77,
                "SubscriberCount": 2,
                "SubscribedCount": 0,
                "SelectedCheer": int(selectedCheer)  
            },
            "PlatformIds": {
                "Platform": 0,
                "PlatformId": 1
            }}
    }

@app.post("/api/platformlogin/v1/getcachedlogins")
@app.post("/api/platformlogin/v1/profiles")
async def profilesv1platformlogin():
    return [{
        "Id": userid,
        "Username": username,
        "DisplayName": username,
        "RegistrationStatus":2,
        "JuniorProfile":False,
        "PendingJunior":False,
        "ForceJuniorImages":False,
        "AvoidJuniors":True,
        "HasBirthday":True,
        "XP": 67,
        "Level": level,
        "Reputation": 0,
        "Verified": True,
        "Developer": True,
        "HasEmail": True,
        "CanReceiveInvites": True,
        "ProfileImageName": "profileimage.png",
        "HasBirthday": True,
        "PhoneLastFour": "RebornRecBlue",
        "EmailEnteredAt": "2025-12-15 17:12:09",
        "PlayerReputation": {
            "Noteriety":0,"CheerGeneral":0,"CheerHelpful":0,"CheerGreatHost":0,
            "CheerSportsman":0,"CheerCreative":0,"CheerCredit":77,
            "SubscriberCount":2,"SubscribedCount":0,"SelectedCheer":int(selectedCheer)
        },
        "PlatformIds":{
            "Platform":0,
            "PlatformId":1
        }
    }]

@app.post("/api/platformlogin/v6")
@app.post("/api/platformlogin/v5")
@app.post("/api/platformlogin/v4")
@app.post("/api/platformlogin/v3")
@app.post("/api/platformlogin/v2")
@app.post("/api/platformlogin/v1")
async def platformloginv1():
    return {
        "Token": "67",
        "PlayerId":userid,
        "Error":"",
        "FirstLoginOfTheDay":True
    }

@app.post("/api/players/v1/list")
async def getplayersdatainbulk(request: Request):
    data = await request.json() 

    player_list = []

    for player_id in data:
        player_data = {
            "Id": player_id,
            "Username": "Discord Message" if player_id == 1 else f"Player{player_id}",
            "DisplayName": "Discord Message" if player_id == 1 else f"Player{player_id}",
            "RegistrationStatus": 2,
            "JuniorProfile": False,
            "PendingJunior": False,
            "ForceJuniorImages": False,
            "AvoidJuniors": True,
            "HasBirthday": True,
            "XP": 67,
            "Level": 99,
            "Reputation": 0,
            "Verified": True,
            "Developer": True,
            "HasEmail": True,
            "CanReceiveInvites": True,
            "ProfileImageName": "discord.png" if player_id == 1 else "otherplayer.png",
            "PhoneLastFour": "RebornRecBlue",
            "EmailEnteredAt": "2025-12-15 17:12:09",
            "PlayerReputation": {
                "Noteriety": 0,
                "CheerGeneral": 0,
                "CheerHelpful": 0,
                "CheerGreatHost": 0,
                "CheerSportsman": 0,
                "CheerCreative": 0,
                "CheerCredit": 77,
                "SubscriberCount": 2,
                "SubscribedCount": 0,
                "SelectedCheer": int(selectedCheer)  
            },
            "PlatformIds": {
                "Platform": 0,
                "PlatformId": 1
            }
        }

        player_list.append(player_data)

    return player_list



@app.post("/api/players/v1/{pid}")
async def eee():
    return []





@app.get("/api/players/v1/{pid}")
async def v1getorcreate(pid: int):
    return {
        "Id": userid,
        "Username": username,
        "DisplayName": username,
        "RegistrationStatus":2,
        "JuniorProfile":False,
        "PendingJunior":False,
        "ForceJuniorImages":False,
        "AvoidJuniors":True,
        "HasBirthday":True,
        "XP": 67,
        "Level": level,
        "Reputation": 0,
        "Verified": True,
        "Developer": True,
        "HasEmail": True,
        "CanReceiveInvites": True,
        "ProfileImageName": "profileimage.png",
        "HasBirthday": True,
        "PhoneLastFour": "RebornRecBlue",
        "EmailEnteredAt": "2025-12-15 17:12:09",
        "PlayerReputation": {
            "Noteriety":0,"CheerGeneral":0,"CheerHelpful":0,"CheerGreatHost":0,
            "CheerSportsman":0,"CheerCreative":0,"CheerCredit":77,
            "SubscriberCount":2,"SubscribedCount":0,"SelectedCheer":int(selectedCheer)
        },
        "PlatformIds":{
            "Platform":0,
            "PlatformId":1
        }
    }

@app.get("/api/config/v2")
async def configv2():
    return configs

@app.get("/api/images/v1/profile/{pid}")
async def imagesv1profile(pid: int):
    return FileResponse(f"{BASE_DIR}\\profileimage.png", media_type="image/png")

@app.get("/api/avatar/v2")
async def avatarv2():
    return avatar

@app.get("/api/settings/v2/")
async def settingsv2():
    return settings

@app.post("/api/settings/v2/set")
async def settingsv2set(request: Request):
    data = await request.json()
    settings_file = os.path.join(BASE_DIR, "settings.txt")
    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            current_settings = json.load(f)
    except:
        current_settings = []
    for item in current_settings:
        if item.get("Key") == data.get("Key"):
            item["Value"] = data.get("Value")
            break
    else:
        current_settings.append({"Key": data.get("Key"), "Value": data.get("Value")})
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(current_settings, f, indent=4)
    global settings
    settings = current_settings
    return []

@app.get("/api/avatar/v3/items")
async def avatarv3items():
    return avataritems

@app.get("/api/avatar/v2/gifts")
async def avatarv2gifts():
    return []

@app.post("/api/avatar/v2/set")
async def avatarv2set(request: Request):
    data = await request.json()
    avatar_file = os.path.join(BASE_DIR, "avatar.txt")
    with open(avatar_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    global avatar
    avatar = data
    return []

@app.post("/api/images/v3/profile")
@app.post("/api/images/v2/profile")
async def upload_profile_image(request: Request, image: UploadFile | None = File(None)):
    path = os.path.join(BASE_DIR, "profileimage.png")
    if image:
        with open(path, "wb") as f: shutil.copyfileobj(image.file, f)
    else:
        body = await request.body()
        if not body: raise HTTPException(status_code=400, detail="No file data received")
        with open(path, "wb") as f: f.write(body)
    return []


@app.get("/api/messages/v2/get")
async def messagesv2get():
    return []

@app.get("/api/relationships/v2/get")
async def relationshipsv2get():
    return []

@app.get("/api/equipment/v1/getUnlocked")
async def equipmentv1getunlocked():
    return [] #equipment

@app.post("/api/images/v1/uploadsaved")
async def upload_saved_image(request: Request, image: UploadFile | None = File(None)):
    photos_dir = os.path.join(BASE_DIR, "Photos")
    os.makedirs(photos_dir, exist_ok=True)

    filename = f"{int(time.time())}.png"
    path = os.path.join(photos_dir, filename)

    if image:
        with open(path, "wb") as f:
            shutil.copyfileobj(image.file, f)
    else:
        body = await request.body()
        if not body:
            return []
        with open(path, "wb") as f:
            f.write(body)

    return {"Success":True,"Error":"","Message":"", "filename":str(filename),"Filename":str(filename)}

@app.post("/api/players/v2/displayname")
async def set_display_name(request: Request):
    body = (await request.body()).decode("utf-8")

    if not body.startswith("Name="):
        return []

    name = body.split("Name=", 1)[1]

    path = os.path.join(BASE_DIR, "Profile", "username.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(name)

    global username
    username = name

    return {"Error":"Please Restart Your Build for name to apply.","Message":"Please Restart Your Build for name to apply.","Success":True,"success":True,"Name":str(username),"name":str(username),"username":str(username),"Username":str(username)}



@app.get("/api/events/v1/list")
async def playerevents():
    return []


@app.get("/api/events/v3/list")
async def eventsv3list():
    return [] # Originally i thought it was {"Created":[],"Responses":[]} but thats
              # for later 2018..


@app.get("/api/playerevents/v1/all")
async def playereventsall():
    return {"Created":[],"Responses":[]}

@app.get("/api/PlayerReporting/v1/moderationBlockDetails")
async def prmodblockdetails():
    return {
        "ReportCategory":0,
        "Duration":0,
        "GameSessionId":0,
        "Message":""
    }

@app.get("/api/config/v1/amplitude")
async def amplitude():
    return {"AmplitudeKey":"RebornRecBlue"}


@app.post("/api/gamesessions/v2/joinrandom")
async def join_random(request: Request):
    body = await request.body()
    data = json.loads(body.decode("utf-8"))

    result = {
        "GameSessionId": str(str(random.randint(1,99999))+"2"),
        "RegionId":"us",
        "RoomId": data["ActivityLevelIds"][0],
        "RecRoomId": None,
        "EventId": None,
        "CreatorPlayerId":userid,
        "Name":"RebornRecBlue Room",
        "ActivityLevelId": data["ActivityLevelIds"][0],
        "Private":False,
        "Sandbox":False,
        "SupportsScreens":True,
        "SupportsVR":True,
        "GameInProgress":False,
        "MaxCapacity":20,
        "IsFull":False
    }


    with open(f"{BASE_DIR}\\gamesession.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(result))


    return {"Result":0,"GameSession":result}


@app.post("/api/gamesessions/v2/create")
async def join_random(request: Request):
    body = await request.body()
    data = json.loads(body.decode("utf-8"))

    block = ["239e676c-f12f-489f-bf3a-d4c383d692c3", 
             "91e16e35-f48f-4700-ab8a-a1b79e50e51b", 
             "acc06e66-c2d0-4361-b0cd-46246a4c455c",
             "949fa41f-4347-45c0-b7ac-489129174045",
             "928ac20b-fe6c-48aa-9286-dcd97ba69d69",
             "7e01cfe0-820a-406f-b1b3-0a5bf575235c"
             ]

    print(data["ActivityLevelId"])

    if data["ActivityLevelId"] in block:
        result = {
        "GameSessionId": str(str(random.randint(1,99999))+"2"),
        "RegionId":"us",
        "RoomId": data["ActivityLevelId"],
        "RecRoomId": None,
        "EventId": None,
        "CreatorPlayerId":userid,
        "Name":"RebornRecBlue Room",
        "ActivityLevelId": data["ActivityLevelId"],
        "Private":False,
        "Sandbox":False,
        "SupportsScreens":True,
        "SupportsVR":True,
        "GameInProgress":False,
        "MaxCapacity":20,
        "IsFull":False
    }
    else:
        result = {
        "GameSessionId": str(str(random.randint(1,99999))+"2"),
        "RegionId":"us",
        "RoomId": data["ActivityLevelId"],
        "RecRoomId": None,
        "EventId": None,
        "CreatorPlayerId":userid,
        "Name":"RebornRecBlue Room",
        "ActivityLevelId": data["ActivityLevelId"],
        "Private":False,
        "Sandbox":True,
        "SupportsScreens":True,
        "SupportsVR":True,
        "GameInProgress":False,
        "MaxCapacity":20,
        "IsFull":False
    }


    with open(f"{BASE_DIR}\\gamesession.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(result))


    return {"Result":0,"GameSession":result}


@app.post("/api/gamesessions/v3/joinroom")
async def join_random(request: Request):
    body = await request.body()
    data = json.loads(body.decode("utf-8"))


    print(data["RoomName"])

    roomdata = rooms[data["RoomName"]]
    
    result = {
        "Result":0,
        "GameSession":roomdata["GameSession"],
        "RoomDetails":roomdata["RoomDetails"]#,
        #"Scenes":roomdata["Scenes"]
    }


    with open(f"{BASE_DIR}\\gamesession.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(result["GameSession"]))


    return result


@img.get("//img/alt/{img}")
@img.get("//img/{img}")
@img.get("/img/{img}")
@img.get("/alt/{img}")
@img.get("/{img}")
async def giveimage(img: str):

    if img == "discord.png":
        image_path = os.path.join(BASE_DIR, "discord.png")

    elif img == "profileimage.png":
        image_path = os.path.join(BASE_DIR, "profileimage.png")

    else:
        image_path = os.path.join(BASE_DIR, "Photos", img)

    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)


@app.get("/api/avatar/v1/saved")
async def avatarv1saved():
    return []

@app.get("/api/objectives/v1/myprogress")
async def objectivesmyprogress():
    return {"Objectives":[{"Index":2,"Group":0,"Progress":0.0,"VisualProgress":0.0,"IsCompleted":False,"IsRewarded":False},{"Index":1,"Group":0,"Progress":0.0,"VisualProgress":0.0,"IsCompleted":False,"IsRewarded":False},{"Index":0,"Group":0,"Progress":0.0,"VisualProgress":0.0,"IsCompleted":False,"IsRewarded":False}],"ObjectiveGroups":[{"Group":0,"IsCompleted":False,"ClearedAt":"2021-04-18T01:59:14.864Z"}]}

@app.get("/api/rooms/v2/myrooms")
@app.get("/api/rooms/v1/myrooms")
async def myrooms():
    return []

@app.get("/api/rooms/v1/mybookmarkedrooms")
async def bookmarked():
    return []

@app.get("/api/consumables/v1/getUnlocked")
async def consumablesv1():
    return consumables

@app.post("/api/objectives/v1/updateobjective")
async def obj():
    return []

@app.get("/api/storefronts/v1/allGiftDrops/2")
async def allgiftdrops():
    return []

@app.get("/api/rooms/v1/myRecent")
async def recentrooms():
    return []

@app.get("/api/gameconfigs/v1/all")
async def gameconfigsall():
    return configsall


@app.post("/api/presence/v1/setplayertype")
async def setplayertype():
    return []

@app.get("/api/avatar/v3/saved")
async def avatarv3saved():
    return []

@app.get("/api/checklist/v1/current")
async def checklistv1current():
    return [{"Order":0,"Objective":400,"Count":3,"CreditAmount":200},{"Order":1,"Objective":1003,"Count":40,"CreditAmount":200},{"Order":2,"Objective":603,"Count":50,"CreditAmount":500},{"Order":3,"Objective":802,"Count":10,"CreditAmount":100},{"Order":4,"Objective":38,"Count":1,"CreditAmount":500},{"Order":5,"Objective":502,"Count":3000,"CreditAmount":150},{"Order":6,"Objective":35,"Count":20,"CreditAmount":100}]

@app.get("//api/chat/v2/myChats")
async def chatv2mychat():
    return []

@app.get("/api/playersubscriptions/v1/my")
async def playersubscriptions():
    return []












# Dont try fixing this. its just an annoying syntax that python does when doing an f string
# you cant put { or } in a f string or whatever you put in it it will think its a variable :(
lb = "{"
rb = "}"


@app.get("/msg/{enum}/{msg}/")
async def sendwsmsg(enum: int, msg: str):
    if not active_ws:
        raise HTTPException(status_code=404, detail="Please Launch Your Build First.")

    await active_ws.send_json(
        {
            "Id":int(enum),
            "Msg":{
                "Id":random.randint(67,676767),
                "FromPlayerId":1,
                "SentTime":math.floor(time.time()),
                "Type":100,
                "Data":str(msg)
            }
        }
    )

    return "Success"



@wsserver.websocket("/api/notification/v2")
async def websocket_endpoint(websocket: WebSocket):
    global active_ws
    await websocket.accept()
    active_ws = websocket
    print(f"WebSocket client connected: {websocket.client}")
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=10)
                print(f"Received from client: {data}")

                data2 = json.loads(data)

                with open(f"{BASE_DIR}\\gamesession.txt", "r", encoding="utf-8") as f:
                    gamesession = f.read()
                    if gamesession == "":
                        gamesession = "null"
                    else:
                        pass

                if data2.get("api") == "playerSubscriptions/v1/update":
                    print(f'{lb}"SessionId":67,"Id":12,"Msg":{lb}"PlayerId":{userid},"IsOnline":true,"InScreenMode":false,"GameSession":{gamesession}{rb}{rb}')
                    await websocket.send_text(f'{lb}"SessionId":67,"Id":12,"Msg":{lb}"PlayerId":{userid},"IsOnline":true,"InScreenMode":false,"GameSession":{gamesession}{rb}{rb}')

                elif data2.get("api") == "heartbeat2":
                    await websocket.send_text(f'{lb}"SessionId":67,"Id":4,"Msg":{lb}"PlayerId":{userid},"IsOnline":true,"InScreenMode":false,"GameSession":{gamesession}{rb}{rb}')

                else:
                    await websocket.send_text('{"SessionId":"67"}')
            except asyncio.TimeoutError:
                await websocket.send_text('{"SessionId":"67"}')
    except WebSocketDisconnect:
        print(f"WebSocket client disconnected: {websocket.client}")



# SignalR btw
@app.websocket("/hub/v1")
async def hub(ws: WebSocket):
    await ws.accept()
    cid = "1"
    clients[cid] = ws

    async def ping():
        while cid in clients:
            try:
                await asyncio.sleep(15)
                await ws.send_text(json.dumps({"type": 6}) + "\x1e")
            except:
                break

    asyncio.create_task(ping())

    try:
        await ws.send_text(json.dumps({"protocol": "json", "version": 1}) + "\x1e")

        while True:
            data = await ws.receive_text()
            for raw in data.split("\x1e"):
                if not raw or raw[0] != "{":
                    continue
                try:
                    msg = json.loads(raw)
                except:
                    continue

                if msg.get("type") != 1:
                    continue

                if msg.get("target") == "SubscribeToPlayers":
                    await ws.send_text(json.dumps({
                        "type": 3,
                        "invocationId": msg.get("invocationId", "0")
                    }) + "\x1e")

                    try:
                        with open(PRESENCE_FILE, "r", encoding="utf-8") as f:
                            presence = json.load(f)
                    except:
                        presence = {}

                    await ws.send_text(json.dumps({
                        "type": 1,
                        "target": "Notification",
                        "arguments": [json.dumps({
                            "Id": "PresenceUpdate",
                            "Msg": presence
                        })]
                    }) + "\x1e")

    except:
        pass
    finally:
        clients.pop(cid, None)

@app.post("/hub/v1/negotiate")
async def negotiate():
    return {
        "negotiateVersion": 0,
        "connectionId": "",
        "availableTransports": [
            {"transport": "WebSockets", "transferFormats": ["Text"]}
        ]
    }











async def startserver():
    import certgen
    cert_path, key_path = certgen.gen_self_signed_cert_files()
    print("\033[H\033[J")
    print("[API Server] Running HTTPS 2001")
    print("[WebSocket Server] Running WS 2002")
    print(CGreen + "Please Startup The Build You'd Like To Play." + "\033[0m")

    api_config = uvicorn.Config(
        app,
        host="localhost",
        port=2001,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
        log_level="info"
    )

    ws_config = uvicorn.Config(
        wsserver,
        host="localhost",
        port=2002,
        log_level="info"
    )

    img_config = uvicorn.Config(
        img,
        host="localhost",
        port=2058,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
        log_level="info"
    )

    img_config_http = uvicorn.Config(
        img,
        host="localhost",
        port=2004,
        log_level="info"
    )

    api_http_config = uvicorn.Config(
    app,
    host="localhost",
    port=2003,
    log_level="info",
    ssl_certfile=None,
    ssl_keyfile=None  # No SSL idk why it wont work.
)


    await asyncio.gather(
        uvicorn.Server(api_config).serve(),
        uvicorn.Server(img_config_http).serve(),
        uvicorn.Server(ws_config).serve(),
        uvicorn.Server(img_config).serve(),
        uvicorn.Server(api_http_config).serve()
    )

if __name__ == "__main__":
    asyncio.run(startserver())
