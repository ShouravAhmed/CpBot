import requests
import json
import os
from bs4 import BeautifulSoup
import shutil
import timeit
from colorama import Fore

import collections
collections.Callable = collections.abc.Callable

import asyncio
import aiofiles as aiof



class OTScraper:
    def __init__(self):
        self.page_htm = None
        self.bts = None
        self.results = list()
        self.session = requests.Session()
        self.cookies = {
            '_ga': 'GA1.2.450165480.1661583992',
            'lightoj-session': '541d7ea71643a8f661b97ff0fff493ecctkt8f%2BH6Zk5LmKBNgPYf0BGRAlk6%2FpNXIq%2BbSKnzTAd2fCBdHxxLstTS%2FZEbJ91J%2BPSWox6CZ5alsz4GcgzWM5YSFkBf8LXXTRXM3Bc%2F1AJI08Ln%2FDUsxRfuSWY0Y%2Bg',
            'XSRF-TOKEN': '150ab679b8817af4656932c1918465dflveFKZWbCY2L8vBICwSQBOoiswn4uPqn018ak20fBCY1lB%2Fk1MviJ6XjplnekfmR0nXuxSK6Ckff0oGGI4CFTlU0U7wFO2c9A6K3wWIz1JaxA82JkocwNzBVumWib%2BJ8',
            'lightoj-session-values': '166040aee4e0d71b15792f52a694213flCAfNwxBmyLQKNlJjZzFbnkpsSeiKBKU%2BEkW6NAJ%2FCewHq4pInmeOawTQY1DewhpLTaa62uLymIBvbsnSE%2BzIBB5UhKRJXxg%2F4%2B37Zj%2FL6rc%2FNzC8S%2F6PmhwL8v7eC0FwV5XhMcS6c8O7xQ0%2FsUuCDxM%2FXBPK2SSDR0H0yHxUEY%3D',
        }
        self.headers = {
            'authority': 'lightoj.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-GB,en;q=0.9,bn-BD;q=0.8,bn;q=0.7,en-US;q=0.6',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'if-none-match': '"241282-LoMu1TJqJUAnI1RvbEG4THg+fGc"',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }

    def fetch(self, url):
        res = self.session.get(url, cookies=self.cookies, headers=self.headers)
        # print(f"HTTP get request to url '{url}' | status code {res.status_code}")
        self.page_htm = res.text
        self.bts = BeautifulSoup(self.page_htm, 'lxml')
        return True

async def getProblemData(id):
    url = "https://lightoj.com/problem/" + str(id)
    sc = OTScraper()
    sc.fetch(url)
    
    ret = {}
    name = sc.bts.find('div', {"class": "title"}).text.strip()
    limit = [x for x in sc.bts.find('div', {"class": "limit-section"}).find_all('span')]
    limit = [x.text.strip() for x in limit if x.text.strip() != ""]    
    sample_testcase = [[y.strip() for y in x.text.split('\n') if y.strip() != ""] for x in sc.bts.find_all('p', {"class":"dataset-container"})]

    ret['url'] = url
    ret["name"] = name
    ret['time limit'] = limit[0].split(' ')[0].strip()
    ret['memory limit'] = limit[1].split(' ')[0].strip()
    ret['id'] = str(id)
    ret['input'] = sample_testcase[0]
    ret['output'] = sample_testcase[1]
    
    print(Fore.GREEN + ret["name"] + " | " +  url + " | Fatched")
    return ret

async def initEnvironment(problem_data, id):
    base_dir = os.getcwd() # os.path.abspath(os.path.join(path, os.pardir))
    path = base_dir + "/LightOJ/" + str(id) 

    if not os.path.exists(path):
        os.makedirs(path)
        os.makedirs(path + "/testcases/")

    async with aiof.open(path + "/ProblemData.json", 'w') as out:
        await out.write(json.dumps(problem_data, indent=2))
                 
    shutil.copy(base_dir + "/CodeTemplate/cf.cpp", path + "/codeA.cpp")
    shutil.copy(base_dir + "/CodeTemplate/loj.cpp", path + "/codeB.cpp")
    shutil.copy(base_dir + "/Script/cpbotloj.py", path + "/cpbot.py")

    async with aiof.open(path + "/testcases/in0", 'w') as out:
        for line in problem_data['input']:
            await out.write(line + "\n")
            
    async with aiof.open(path + "/testcases/out0", 'w') as out:
        for line in problem_data['output']:
            await out.write(line + "\n")
    

async def InitLightOJProblem(id):
    start = timeit.default_timer()
    try:
        problem_data = asyncio.create_task(getProblemData(id))
    except:
        print(Fore.RED + "Problem Doesn't Exist.")
        return

    problem_data = await problem_data
    await asyncio.create_task(initEnvironment(problem_data, id))
    
    print(Fore.RED + 'Execution Time: ', timeit.default_timer() - start) 


if __name__ == "__main__":
    InitLightOJProblem()
