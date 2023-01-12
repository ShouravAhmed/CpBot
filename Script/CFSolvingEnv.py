import requests
import json
import os
from bs4 import BeautifulSoup
import shutil
import timeit
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
import asyncio
import aiofiles as aiof


class OTScraper:
    def __init__(self):
        self.cookies = {
            'RCPC': '2127f8006d7dfa9faac884a68f2e2790',
        }
        self.headers = {
            'authority': 'codeforces.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-GB,en;q=0.9',
            'dnt': '1',
            'referer': 'https://codeforces.com/contest/1760/problem/C',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        self.params = {
            'f0a28': '1',
        }
        self.page_htm = None
        self.bts = None
        self.results = list()
        self.session = requests.Session()
        
    def fetch(self, url):
        res = self.session.get(url, params=self.params, cookies=self.cookies, headers=self.headers)
        # print(f"HTTP get request to url '{url}' | status code {res.status_code}")
        self.page_htm = res.text
        self.bts = BeautifulSoup(self.page_htm, 'lxml')
        return True

async def FetchCodeForcesProblem(url, sc):
    sc.fetch(url)
    return sc.bts

async def getContestData(id):
    url = "https://codeforces.com/contest/" + str(id)
    sc = OTScraper()
    
    sc.fetch(url)
    problems = sc.bts.find("table", {"class":"problems"})
    data = [problem.find_all('td') for problem in problems.find_all('tr')]
    
    problem_urls = []
    solve_counts = {}
    
    for d in data:
        if len(d):
            probUrl = "https://codeforces.com" + d[1].find('a')['href']
            problem_urls.append(probUrl)
            solve_counts[probUrl] = int(d[3].text.strip().split('x')[1].strip())
    
    contest_data = dict()

    def ProcessCodeForcesProblem(bts):
        sampleTest = bts.find("div", {"class":"sample-tests"})
        all_input = sampleTest.find_all("div", {"class":"input"})
        all_output = sampleTest.find_all("div", {"class":"output"})
        
        sampleio = list()
        
        for i in range(len(all_input)):
            inp = all_input[i]
            outp = all_output[i]
            
            inpdiv = inp.find("pre").find_all("div")
            if len(inpdiv) > 0:
                inp = [line.text.strip() for line in inpdiv]
            else:
                inp = [x.strip() for x in inp.find('pre').text.split('\n') if x.strip() != ""]

            outp = [x.strip() for x in outp.find('pre').text.split('\n') if x.strip() != ""]
        
            sampleio.append( 
                {
                    "input": inp, 
                    "output": outp
                }
            )
        problem_data = dict()
        problem_data['index'] = bts.find('div', {"class":"title"}).text.strip().split('.')[0].strip()
        problem_data['name'] = bts.find('div', {"class":"title"}).text.strip().split('.')[1].strip()
        probUrl = url + "/problem/" + problem_data['index']
        problem_data['url'] = probUrl
        problem_data['tags'] = [tag.text.strip() for tag in bts.find_all('span', {"class":"tag-box"})]
        problem_data['sampleio'] = sampleio
        problem_data['solve count'] = solve_counts[probUrl]
        contest_data[problem_data['index']] = problem_data
        print(Fore.GREEN + probUrl + " | Fatched.")

    taskList = []
    for probUrl in problem_urls:
        taskList.append(asyncio.create_task(FetchCodeForcesProblem(probUrl, sc)))
    
    sampleTests = []
    for task in taskList:
        sampleTest = await task
        sampleTests.append(sampleTest)
    
    for sampleTest in sampleTests:
        ProcessCodeForcesProblem(sampleTest)
    
    return contest_data

def InitDemoContest(id):
    base_dir = os.getcwd()    
    path = base_dir + "/CodeForces/" + str(id) 

    if not os.path.exists(path):
        os.makedirs(path)
    contest_data = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'}
    
    for index in contest_data:
        if not os.path.exists(path + "/" + index):
            os.makedirs(path + "/" + index)
        if not os.path.exists(path + "/" + index  + "/testcases/"):
            os.makedirs(path + "/" + index + "/testcases/")
        
        shutil.copy(base_dir + "/CodeTemplate/cf.cpp", path + "/" + index + "/code" + index + ".cpp")
        shutil.copy(base_dir + "/Script/cpbotcf.py", path + "/" + index + "/cpbot.py")
        
        sampleios = [{'input':'', 'output':''}]
        for i in range(len(sampleios)):
            
            sampleio = sampleios[i]
            with open(path + "/" + index + "/testcases/in" + str(i), 'w') as f:
                for line in sampleio['input']:
                    f.write(line + "\n")
            with open(path + "/" + index + "/testcases/out" + str(i), 'w') as f:
                for line in sampleio['output']:
                    f.writelines(line + "\n")
        
async def initEnvironment(contest_data, id):
    path = os.getcwd()
    
    base_dir = path # os.path.abspath(os.path.join(path, os.pardir))
    path = base_dir + "/CodeForces/" + str(id) 

    if not os.path.exists(path):
        os.makedirs(path)
        
    async with aiof.open(path + "/contestData.json", "w") as out:
        await out.write(json.dumps(contest_data, indent=2))
    
    for index, problem_details in contest_data.items():
        if not os.path.exists(path + "/" + index):
            os.makedirs(path + "/" + index)
        if not os.path.exists(path + "/" + index  + "/testcases/"):
            os.makedirs(path + "/" + index + "/testcases/")
        
        shutil.copy(base_dir + "/CodeTemplate/cf.cpp", path + "/" + index + "/code" + index + ".cpp")
        shutil.copy(base_dir + "/Script/cpbotcf.py", path + "/" + index + "/cpbot.py")
        
        sampleios = problem_details["sampleio"]
        
        for i in range(len(sampleios)):
            sampleio = sampleios[i]
            
            async with aiof.open(path + "/" + index + "/testcases/in" + str(i), 'w') as out:
                for line in sampleio['input']:
                    await out.write(line + "\n")
                    
            async with aiof.open(path + "/" + index + "/testcases/out" + str(i), 'w') as out:
                for line in sampleio['output']:
                    await out.write(line + "\n")
                    
        
async def InitCodeForcesContest(id):
    start = timeit.default_timer()
    try:
        contest_data = asyncio.create_task(getContestData(id))
    except:
        print(Fore.RED + "Contest Doesn't Exist.") # InitDemoContest(id)
        return

    contest_data = await contest_data
    print(Fore.RED + 'Execution Time: ', timeit.default_timer() - start) 

    await asyncio.create_task(initEnvironment(contest_data, id))
                    

if __name__ == "__main__":
    InitCodeForcesContest()
