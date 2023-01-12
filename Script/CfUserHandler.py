import os
import json
from colorama import Fore
import requests

class GetJSON:
    def __init__(self):
        self.hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        self.session = requests.Session()
        self.json = None

    def fetch(self, url):
        try:
            with self.session.get(url, headers = self.hdr) as responce:
                self.json = responce.json()
        except:
            pass

def isValidUser(handle):
    userinfo = GetJSON()
    userinfo.fetch("https://codeforces.com/api/user.info?handles=" + handle)
    return userinfo.json["status"] == "OK"

def process(command, username=None):
    if username and not isValidUser(username):
        print(Fore.RED + "Invalid User Handle")
        return
    
    path = os.getcwd() + "/Script/cfuser.json"
    userData = dict()

    def write():
        with open(path, 'w') as f:
            f.write(json.dumps(userData, indent=2))
    def read():
        with open(path, 'r') as f:
            return json.load(f)
    if not os.path.exists(path):
        write()

    userData = read()
    if command == "add":
        print(Fore.GREEN + "\nUser '" + username + "' Added Successfully!")
        if username not in userData:
            userData[username] = False
    elif command == "remove":
        print(Fore.GREEN + "\nUser '" + username + "' Removed Successfully.")
        if username in userData:
            del userData[username]
    elif command == "set-primary":
        print(Fore.GREEN + "\nUser '" + username + "' Set as Primary User.")
        for i, j in userData.items():
            userData[i] = False
        userData[username] = True
    elif command == "check":
        print(Fore.RED + "\n" + "Codeforces Users\n")
        x = 1
        for i,j in userData.items():
            if j:
                print(Fore.BLUE + str(x) + ". " + i + " : " + Fore.GREEN + "(Primary User)")
            else:
                print(Fore.BLUE + str(x) + ". " + i)
            x += 1        
    else:
        print(Fore.GREEN + "\npython cpbot.py --cfuser argument:value\n")
        print(Fore.RED + "Arguments are:")
        print(Fore.BLUE + " 1. add:username")
        print(Fore.BLUE + " 2. set-primary:username" + Fore.GREEN + " Your currently active account.")
        print(Fore.BLUE + " 3. remove:username")
        print(Fore.BLUE + " 4. check")    
        
    write()
    