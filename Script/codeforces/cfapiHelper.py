import os
from colorama import Fore
import orjson
import aiofiles as aiof
import asyncio
import cfapi

async def getRankList():
    if os.path.exists('GlobalRankList.json'):
        async with aiof.open('GlobalRankList.json', mode='r') as fs:
            content = await fs.read()
            ret = orjson.loads(content)
            if "RankList" in ret:
                print(Fore.YELLOW + "\n----------------------------------")
                print(Fore.BLUE + "CodeForces Global RankList Fetched")
                print(Fore.LIGHTMAGENTA_EX + "Currently there are total", len(ret["RankList"]), "user in CodeForces.")
                print(Fore.YELLOW + "----------------------------------")
                return ret['RankList']
            
    print(Fore.YELLOW + "\n----------------------------------")
    print(Fore.GREEN + "CodeForces Population")
    print(Fore.YELLOW + "----------------------------------")
    print(Fore.RED + "Sorry no data found.\nPlease wait we are loading the data.")
    print(Fore.YELLOW + "----------------------------------\n")
    
    GlobalRankList = asyncio.create_task(cfapi.FetchGlobalRankList())
    await GlobalRankList
    return None

async def getPopulation():
    if os.path.exists('GlobalRankList.json'):
        async with aiof.open('GlobalRankList.json', mode='r') as fs:
            content = await fs.read()
            ret = orjson.loads(content)
            if "Population" in ret:
                for season, data in ret['Population'].items():
                    print(Fore.YELLOW + "\n----------------------------------")
                    print(Fore.GREEN + "CodeForces " + season + " Population")
                    print(Fore.YELLOW + "----------------------------------")
                    for rank, count in data.items():
                        print(Fore.BLUE + rank, " :", count)
                    print(Fore.YELLOW + "----------------------------------\n")
                return ret['Population']
            
    print(Fore.YELLOW + "\n----------------------------------")
    print(Fore.GREEN + "CodeForces Population")
    print(Fore.YELLOW + "----------------------------------")
    print(Fore.RED + "Sorry no data found.\nPlease wait we are loading the data.")
    print(Fore.YELLOW + "----------------------------------\n")
    
    GlobalRankList = asyncio.create_task(cfapi.FetchGlobalRankList())
    await GlobalRankList
    return None

async def getUserRating():
    if os.path.exists('userData.json'):
        async with aiof.open('userData.json', mode='r') as fs:
            content = await fs.read()
            ret = orjson.loads(content)
            if "User" in ret:
                if len(ret['User']) > 0:
                    return ret['User']
            
    print(Fore.YELLOW + "----------------------------------")
    print(Fore.RED + "Sorry no user data found.\nPlease add CodeForces user.")
    print(Fore.YELLOW + "----------------------------------\n")
    
    return None

async def getUserColor(rating):
    if rating < 1200:
        return 'gray'
    elif rating < 1400:
        return 'green'
    elif rating < 1600:
        return 'cyan'
    elif rating < 1900:
        return 'blue'
    elif rating < 2100:
        return 'pink'
    elif rating < 2300:
        return 'yellow'
    elif rating < 2400:
        return 'orange'
    elif rating < 2600:
        return 'lightcoral'
    elif rating < 3000:
        return 'red'
    else:
        return 'darkred'

