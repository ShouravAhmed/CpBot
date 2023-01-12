from curses.ascii import isdigit
from Script import CFSolvingEnv
from Script import UpcommingContest
from Script import CodeForcesLive
from Script import LojSolvingEnv
from Script import SolvingEnv
from Script import Careers
from Script import CfUserHandler
import fire
from colorama import Fore
import asyncio


def RunScript(initcf="", upcomming="", help="", cflive="", initloj="", initcode="", career="", **kwargs):
    initcf = str(initcf)
    initloj = str(initloj)
    initcode = str(initcode)
    
    if initcf.isdigit():
        asyncio.run(CFSolvingEnv.InitCodeForcesContest(initcf))
    elif upcomming != "":
        UpcommingContest.getUpcommingContests(upcomming)
    elif cflive == True or cflive == 'reset':
        asyncio.run(CodeForcesLive.CFLive(cflive))
    elif initloj.isdigit():
        asyncio.run(LojSolvingEnv.InitLightOJProblem(initloj))
    elif initcode != "True" and len(initcode) > 0:
        SolvingEnv.InitSolvingEnv(initcode)
    elif career == True or career != "":
        if career == True:
            career = ""
        asyncio.run(Careers.GetCareerData(career))
    elif help == True:
        print(Fore.GREEN + "\npython cpbot.py --argument value\n")
        print(Fore.RED + "Arguments are:")
        print(Fore.BLUE + " 1. Init CodeForces Contest:" + Fore.GREEN + " python cpbot.py --initcf contest_id")
        print(Fore.BLUE + " 2. Init LightOJ Problem:" + Fore.GREEN + " python cpbot.py --initloj problem_id")
        print(Fore.BLUE + " 3. Upcomming Contests:" + Fore.GREEN + " python cpbot.py --upcomming oj_name")
        print(Fore.BLUE + " 4. Start CodeForces Live:" + Fore.GREEN + " python cpbot.py --cflive reset")
        print(Fore.BLUE + " 5. Create Solving Environment for a Problem:" + Fore.GREEN + " python cpbot.py --initcode problem_name")
        print(Fore.BLUE + " 6. Software Companies Details:" + Fore.GREEN + " python cpbot.py --career company_name")
        print(Fore.BLUE + " 4. Codeforces Chase List:" + Fore.GREEN + " python cpbot.py --cfuser")
    elif "cfuser" in kwargs:
        inp = kwargs["cfuser"]
        if inp == True:
            print(Fore.RED + "For Details:" + Fore.GREEN + " python cpbot.py --cfuser help")    
        else:
            ls = [x.lower() for x in inp.split(':')]
            if ls[0] == 'help' or ls[0]=='check':
                CfUserHandler.process(ls[0])
            elif len(ls) == 2 and (ls[0] == 'add' or ls[0] == 'set-primary' or ls[0] == 'remove'):
                CfUserHandler.process(ls[0], ls[1])
            else:
                print(Fore.RED + "For Details:" + Fore.GREEN + " python cpbot.py --cfuser help")    
    else:
        print(Fore.RED + "For Details:" + Fore.GREEN + " python cpbot.py --help")

def main():
    fire.Fire(RunScript)

if __name__ == "__main__":
    main()
