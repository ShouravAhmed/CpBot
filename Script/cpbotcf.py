from curses.ascii import isdigit
from re import sub
import subprocess
import os
from colorama import Fore
import fire
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.getcwd() , os.pardir)) , os.pardir)) , os.pardir))
sys.path.append(BASE_DIR)
from Script import UpcommingContest
from Script import CompileAndRun
from Script import SubmitCF
from Script import CodeForcesLive
from Script import Careers

def RunScript(upcomming="", run="", submit="", help="", cflive="", career="", **kwargs):
    if upcomming != "":
        UpcommingContest.getUpcommingContests(upcomming)
    elif run != "":
        CompileAndRun.compile_and_run(run)
    elif cflive == True:
        os.chdir(BASE_DIR)
        CodeForcesLive.CFLive()
    elif help == True:
        print(Fore.GREEN + "\npython cpbot.py --argument value\n")
        print(Fore.RED + "Arguments are:")
        print(Fore.BLUE + " 1. Run Code and Test With Sample Cases:" + Fore.GREEN + " python cpbot.py --run O2 " + Fore.BLUE + "| O2 for Memory Sanitizer.")
        print(Fore.BLUE + " 2. Start CodeForces Live:" + Fore.GREEN + " python cpbot.py --cflive")
        print(Fore.BLUE + " 3. Upcomming Contests:" + Fore.GREEN + " python cpbot.py --upcomming oj_name")
    else:
        print(Fore.RED + "For Details:" + Fore.GREEN + " python cpbot.py --help")

                
if __name__ == "__main__":
    fire.Fire(RunScript)
