import requests
import json
import os
from bs4 import BeautifulSoup
import shutil
import timeit
from colorama import Fore

def InitSolvingEnv(id):
    
    base_dir = os.getcwd()
    path = base_dir + "/Code/" + id 

    if not os.path.exists(path):
        os.makedirs(path)
        os.makedirs(path + "/testcases/")

    
    shutil.copy(base_dir + "/CodeTemplate/loj.cpp", path + "/codeA.cpp")
    shutil.copy(base_dir + "/CodeTemplate/cf.cpp", path + "/codeB.cpp")
    shutil.copy(base_dir + "/Script/cpbotloj.py", path + "/cpbot.py")

    with open(path + "/testcases/in0", 'w') as f:
        f.write("\n")
    with open(path + "/testcases/out0", 'w') as f:
        f.writelines("\n")
    
    print(Fore.LIGHTMAGENTA_EX + "Solving Environment Created for " + Fore.YELLOW + "[" + id + "]")
    print(Fore.GREEN + "Path: " + Fore.RED + path)

if __name__ == "__main__":
    InitSolvingEnv("sample-problem")
