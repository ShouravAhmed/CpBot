from cProfile import label
import json
from operator import mod, truediv
from textwrap import indent
from turtle import color
import time
import asyncio
from colorama import Fore
import colorama
import orjson
import aiofiles as aiof

from datetime import datetime
import os

import matplotlib.pyplot as plot
import cfapiHelper


async def timeLog():
    try:
        while True:
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            await asyncio.sleep(1)
    except:
        pass


async def PlotUserPositionInGlobalRankList():
    rankList = asyncio.create_task(cfapiHelper.getRankList())
    users = asyncio.create_task(cfapiHelper.getUserRating())
    rankList = await rankList
    users = await users
    
    if rankList is None:
        return
    data = [x["MaxRating"] for x in rankList]
    
    plot.style.use('ggplot')
    bins = [x for x in range(0,max(data)+100,100)]
    colors = []
    for rating in bins:
        color.append(cfapiHelper.getUserColor(rating))
            
    cnts, values, bars = plot.hist(data, bins=bins, edgecolor='black')
    
    for i, (cnt, value, bar) in enumerate(zip(cnts, values, bars)):
        bar.set_facecolor(colors[i + 1])
    
    for user in users:
        plot.axvline(user['rating'], color=cfapiHelper.getUserColor(user['rating']), label=user['handle'])
    
    plot.legend()
    
    plot.title("CodeForces Global Rank Distribution")
    plot.xlabel("Rating")
    plot.ylabel("Population")
    plot.tight_layout()
    
    plot.show()
    

    
# ------------------------------------------------------------------------------
async def main():
    timelog = asyncio.create_task(timeLog())
    rank = asyncio.create_task(PlotUserPositionInGlobalRankList())
    await rank


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    asyncio.run(main())

