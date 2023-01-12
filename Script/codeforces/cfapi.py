#!/usr/bin/python
# -*- coding: utf-8 -*-
from logging import exception
import time
import orjson
import json
import requests
from colorama import Fore
import os
import asyncio
import aiofiles as aiof

async def FetchGlobalRankList():
    async def RedundantFetch():
        if os.path.exists('GlobalRankList.json'):
            async with aiof.open('GlobalRankList.json', mode='r') as fs:
                content = await fs.read()
                data = orjson.loads(content)
                if "Fetching" in data:
                    return True
        async with aiof.open("GlobalRankList.json", "w") as out:
            await out.write(json.dumps({'Fetching':True}))
        return False
                
    async def fetch(url):
        start_time = time.time()
        hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        responce = requests.get(url, stream=True, headers=hdr)
        
        print(Fore.YELLOW + "\n----------------------------------")
        if responce.status_code == 200:
            print(Fore.GREEN + "GlobalRankList | fetched | %s seconds" % (time.time() - start_time))
        else:
            print(Fore.RED + "GlobalRankList | fetch error : {responce.status_code}")
        print(Fore.YELLOW + "----------------------------------\n")
        
        return responce
    
    async def process(responce):
        start_time = time.time()
        print(Fore.YELLOW + "\n----------------------------------")
        print(Fore.RED + "Processing | GlobalRankList Data")
        print(Fore.YELLOW + "----------------------------------\n")
        
        async with aiof.open("tmp.json", "wb") as out:
            for chunk in responce:
                await out.write(chunk)
            out.flush()

        async with aiof.open('tmp.json', mode='rb') as inp:
            contents = await inp.read()
            ret = orjson.loads(contents)
            os.remove("tmp.json")
            
            print(Fore.YELLOW + "\n----------------------------------")
            print(Fore.GREEN + "GlobalRankList Data | Processed Successfully | %s seconds" % (time.time() - start_time))
            print(Fore.YELLOW + "----------------------------------\n")
            
            return ret

    async def save(js):
        start_time = time.time()
        print(Fore.YELLOW + "\n----------------------------------")
        print(Fore.RED + "Saving | GlobalRankList Data")
        print(Fore.YELLOW + "----------------------------------\n")
        
        ret = {
            'TotalUser': 0,
            'Population': {
                'Current': {},
                'Max': {}
            },
            'RankList': []
        }
        
        for user in js['result']:
            ret['TotalUser'] += 1
            ret['Population']['Current'][user['rank']] = ret['Population']['Current'].get(user['rank'], 0) + 1
            ret['Population']['Max'][user['maxRank']] = ret['Population']['Max'].get(user['maxRank'], 0) + 1

            ret['RankList'].append(
                {
                    'Handle': user['handle'],
                    'Country': (user['country'] if 'country' in user else None),
                    'Organization': (user['organization'] if 'organization' in user else None),
                    'MaxRating': user['maxRating'],
                    'CurrentRating': user['rating'],
                }
            )
        
        async with aiof.open("GlobalRankList.json", "w") as out:
            await out.write(json.dumps(ret))
            
        print(Fore.YELLOW + "\n----------------------------------")
        print(Fore.GREEN + "GlobalRankList Data | Saved Successfully | %s seconds" % (time.time() - start_time))
        print(Fore.YELLOW + "----------------------------------\n")
    
    try:
        redundant = await asyncio.create_task(RedundantFetch())
        if redundant:
            return
        
        start_time = time.time()
        print(Fore.YELLOW + "\n----------------------------------")
        print(Fore.RED + "Fetching CodeForces Global RankList")
        print(Fore.YELLOW + "----------------------------------\n")
        
        responce = await asyncio.create_task(fetch('https://codeforces.com/api/user.ratedList'))
        js = await asyncio.create_task(process(responce))
        await asyncio.create_task(save(js))
        
        print(Fore.YELLOW + "\n----------------------------------")
        print(Fore.GREEN + "CodeForces Global RankList Fetched Successfully  | %s seconds" % (time.time() - start_time))
        print(Fore.YELLOW + "----------------------------------\n")
        
    except exception as e:
        print(Fore.YELLOW + "\n----------------------------------")
        print(Fore.RED + "GlobalRankList Data | exception : " + e)
        print(Fore.YELLOW + "----------------------------------\n")
