import requests
import json
import time
from colorama import Fore
import datetime

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


def getUpcommingContests(name):
    apiLinks = {
        "all": "https://kontests.net/api/v1/all",
        "topcoder": "https://kontests.net/api/v1/top_coder",
        "atcoder": "https://kontests.net/api/v1/at_coder",
        "codechef": "https://kontests.net/api/v1/code_chef",
        "csacademy": "https://kontests.net/api/v1/cs_academy",
        "hackerrank": "https://kontests.net/api/v1/hacker_rank",
        "hackerearth": "https://kontests.net/api/v1/hacker_earth",
        "kickstart": "https://kontests.net/api/v1/kick_start",
        "leetcode": "https://kontests.net/api/v1/leet_code",
        "codeforces": "https://kontests.net/api/v1/codeforces",
        "cfgym": "https://kontests.net/api/v1/codeforces_gym"
    }
    
    if name == True or name not in apiLinks:
        print(Fore.BLUE + "------------------------------------------")
        print(Fore.RED + "Not a valid OJ.")
        print(Fore.BLUE + "------------------------------------------")
        print(Fore.GREEN + "Available OJ's are: ", end = "")
        for a, b in apiLinks.items():
            if a == "all":
                continue
            print(a, end=" | ")
        print("")
        print(Fore.BLUE + "------------------------------------------")
        return            

    data = GetJSON()
    data.fetch(apiLinks[name])
    
    if data.json is None:
        print(Fore.RED + "Can't fetch the data.")
    else:
        print(Fore.YELLOW + "---------------------------------------------------------------")
        print(Fore.BLUE + "Upcomming Contest List")
        print(Fore.YELLOW + "---------------------------------------------------------------")
        idx = 1
        for contest in data.json:
            timezone = int(str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo))
            contest_date_time = " ".join(contest["start_time"].split('T')).replace('Z', ' ')
            contest_date_time = ' '.join(contest_date_time.split(' ')[:2])
            contest_date_time = contest_date_time.split('.')[0]

            contest_date_time = datetime.datetime.strptime(contest_date_time, '%Y-%m-%d %H:%M:%S')
            contest_date_time = contest_date_time + datetime.timedelta(hours=timezone)
            contest_date_time = contest_date_time.strftime("%d %B %Y - %I:%M %p")

            print(Fore.BLUE + str(idx) + ". " + contest["name"] + Fore.LIGHTMAGENTA_EX + " | " + (contest["site"] if name=="all" else name.title()) + " | " + Fore.YELLOW + contest_date_time)
            print(Fore.GREEN + "".join([" " for x in str(idx)]) + "  " + contest["url"])
            print(Fore.YELLOW + "---------------------------------------------------------------")
            idx = idx + 1



