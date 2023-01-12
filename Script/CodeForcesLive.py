import os
import json
from textwrap import indent
import requests
from colorama import Fore
from gtts import gTTS
from playsound import playsound 
import random
import time
import sys
import math

import asyncio
import aiofiles as aiof

import threading
from concurrent.futures import ThreadPoolExecutor


async def TextToSpeech(texts):
    for text in texts:
        audio = gTTS(text=text, lang="en", slow=False)
        audio.save("tts.mp3")
        playsound("tts.mp3")
        os.remove("tts.mp3")

async def playWin():
    path = os.getcwd() + "/Script/soundeffect/win"
    files = os.listdir(path)
    playsound(path + "/" + random.choice(files))

async def playlose():
    path = os.getcwd() + "/Script/soundeffect/lose"
    files = os.listdir(path)
    playsound(path + "/" + random.choice(files))

async def data_manager(path, data, op):
    async def write():
        async with aiof.open(path, mode='w') as dta:
            await dta.write(json.dumps(data, indent=2))
            
    async def read():
        async with aiof.open(path, mode='r') as dta:
            ret = await dta.read()
            return json.loads(ret)
    
    if not os.path.exists(path):
        await write()
    
    if op == 'read':
        return await read()
    else:
        await write()

async def get_submissions(user, render = False, past_submissions = None, new_submissions = None, anounce_queue = None, primary_user = None):
    cf = {}
    with requests.get("https://codeforces.com/api/user.status?handle=" + user) as responce:
        cf = responce.json()
    ret = {}
    ret['user'] = user
    ret['submissions'] = {}
    
    for data in cf["result"]:
        try:
            ret['submissions'][data["id"]] = {
                "id": data["id"],
                "contest": str(data["problem"]["contestId"]) if "contestId" in data["problem"] else None,
                "index": data["problem"]["index"],
                "name": data["problem"]["name"],
                "passed testcase": data["passedTestCount"],
                "runtime": data["timeConsumedMillis"]
            } 
            if "verdict" not in data:
                ret['submissions'][data["id"]]["verdict"] = "In Queue"
            elif (" ".join(data["verdict"].split('_')).title()) == "Ok":
                ret['submissions'][data["id"]]["verdict"] = "Accepted"
            else:
                ret['submissions'][data["id"]]["verdict"] = (" ".join(data["verdict"].split('_')).title())
            
        except Exception as e:
            print("Exception: ", e)
            print(json.dumps(data, indent=2))
    
    if render:
        for submission in ret['submissions']:
            if ret["user"] not in past_submissions or str(submission) not in past_submissions[ret["user"]]["submissions"]:
                if ret["user"] not in new_submissions or submission not in new_submissions[ret["user"]]["submissions"]:
                    ret['submissions'][submission]["user"] = ret["user"]
                    anounce_queue.append(ret['submissions'][submission])
        
        await show_submissions(primary_user, new_submissions, anounce_queue)
    else:
        return ret

async def get_current_submissions(users, past_submissions):
    cfsubmissions = {}    
    tasks = []
    
    for user in users:
        tasks.append(asyncio.create_task(get_submissions(user)))

    for task in tasks:
        data = await task
        cfsubmissions[data['user']] = data
        past_submissions[data['user']] = data
    
    await data_manager(os.getcwd() + "/Script/cfusersubmissions.json", cfsubmissions, "write")
    

async def show_submissions(primary_user, new_submissions, original_anounce_queue):
    try:
        os.system('clear')
        if len(new_submissions.items()) == 0:
            print(Fore.BLUE + "============================================================================")
            print(Fore.BLUE + "----------------------------------------------------------------------------")
            print(Fore.RED + "                No New Submission Found")
            print(Fore.BLUE + "----------------------------------------------------------------------------")
            print(Fore.BLUE + "============================================================================")
            
        for user in new_submissions:
            print(Fore.MAGENTA + "----------------------------------------------------------------------------")
            print(Fore.BLUE +    "============================================================================")
            print(Fore.MAGENTA + " " + user)
            print(Fore.BLUE + "============================================================================")
            
            for key, submission in new_submissions[user]["submissions"].items():
                sub = []
            
                s = submission['contest'] + submission['index']
                x = int(((7 - len(s)) / 2))
                for i in range(x):
                    s = " " + s
                for i in range(x):
                    s = s + " "
                while len(s) < 7:
                    s = s + " "
                sub.append(s)
                
                s = submission['name']
                if len(s) > 25:
                    s = s[0:25]
                x = int(((25 - len(s)) / 2))
                for i in range(x):
                    s = " " + s
                for i in range(x):
                    s = s + " "
                while len(s) < 25:
                    s = s + " "
                sub.append(s)
                
                s = submission['verdict']
                if len(s) > 15:
                    s = s[0:15]
                x = int(((15 - len(s)) / 2))
                for i in range(x):
                    s = " " + s
                for i in range(x):
                    s = s + " "
                while len(s) < 15:
                    s = s + " "
                sub.append(s)
                
                s = "(case:" + str(submission['passed testcase']) + ")"
                x = int(((10 - len(s)) / 2))
                for i in range(x):
                    s = " " + s
                for i in range(x):
                    s = s + " "
                while len(s) < 10:
                    s = s + " "
                sub.append(s)
                
                s = "(time:" + str(submission['runtime']) + ")"
                x = int(((10 - len(s)) / 2))
                for i in range(x):
                    s = " " + s
                for i in range(x):
                    s = s + " "
                while len(s) < 10:
                    s = s + " "
                sub.append(s)
                
                if submission['verdict'] == 'Accepted':
                    print(Fore.GREEN + '|'.join(sub))
                else:
                    print(Fore.RED + '|'.join(sub))
                print(Fore.BLUE + "============================================================================")
                
        anounce_queue = original_anounce_queue.copy()
        original_anounce_queue.clear()
        
        for anounce in anounce_queue:  
            user = anounce["user"]
            anounce.pop("user", None)
            
            await TextToSpeech([''.join([x for x in user if x.isalpha()]), " submited a new solution."])
            
            if anounce["verdict"] == "In Queue":
                texts = [
                    "Problem " + anounce["index"] + " " + anounce["name"] + " is, In Queue."
                ]
                await TextToSpeech(texts)
            elif anounce["verdict"] == "Testing":
                texts = [
                    "Problem " + anounce["index"] + " " + anounce["name"] + " is being tested, " + str(anounce["passed testcase"]) + " TestCase Passed"
                ]
                await TextToSpeech(texts)
            else:
                if user not in new_submissions:
                    new_submissions[user] = {
                        'user' : user,
                        "submissions" : {}
                    }
                new_submissions[user]["submissions"][anounce["id"]] = anounce
                
                if anounce["verdict"] == "Accepted":
                    if user == primary_user:
                        await playWin()
                    texts = [
                        "Problem " + anounce["index"] + " " + anounce["name"] + " got Accepted", 
                        str(anounce["passed testcase"]) + " TestCase Passed with Runtime " + str(anounce["runtime"]) + " milisecond"
                    ]
                    await TextToSpeech(texts)
                else:
                    await playlose()
                    texts = [
                        "Problem " + anounce["index"] + " " + anounce["name"], 
                        "Got " + anounce["verdict"] + " on testcase " + str(anounce["passed testcase"] + 1)
                    ]
                    await TextToSpeech(texts)
    except Exception as e:
        print("Exception: ", e)
        

async def update_submissions(users, past_submissions, new_submissions, anounce_queue):
    try:
        while True:
            for user in users:
                if user in past_submissions and user != users[0]:
                    asyncio.create_task(get_submissions(user, True, past_submissions, new_submissions, anounce_queue, users[0]))
                if users[0] in past_submissions and users[0] != "":
                    asyncio.create_task(get_submissions(users[0], True, past_submissions, new_submissions, anounce_queue, users[0]))
            await asyncio.sleep(3)
            
    except Exception as e:
        print("Exception: ", e)
    
async def get_users_list():
    users = await data_manager(os.getcwd() + "/Script/cfuser.json", {}, "read")
    primary_user = [x for x in users if users[x] == True]
    users = [x for x in users if users[x] != True]
    if len(primary_user) > 0:
        users.insert(0, primary_user[0])
    else:
        users.insert(0, "")
    return users

async def CFLive(arg):
    try:
        users = await get_users_list()
        
        past_submissions = {}
        new_submissions = {}
        anounce_queue = []
        
        async_tasks = []
        
        if arg == 'reset':
            async_tasks.append(asyncio.create_task(get_current_submissions(users, past_submissions)))
        else:
            past_submissions = await asyncio.create_task(data_manager(os.getcwd() + "/Script/cfusersubmissions.json", {}, 'read'))
        
        async_tasks.append(asyncio.create_task(update_submissions(users, past_submissions, new_submissions, anounce_queue)))
        
        for task in async_tasks:
            await task
    except Exception as e:
        print("Exception:", e)

if __name__ == "__main__":
    CFLive()
