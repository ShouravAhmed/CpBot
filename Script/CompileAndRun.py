import os
from colorama import Fore
import fire
import sys
import subprocess


def compile_and_run(run):
    path = os.getcwd()
    files = os.listdir()
    
    for f in files:
        if "cpp" in f:
            cpp_file_path = os.path.join(path, f)
    
    print(Fore.LIGHTMAGENTA_EX + "Compiling: " + cpp_file_path.split('/')[-1])

    if run == True:
        gcc_compile = subprocess.run(["g++", "-std=c++17", "-Wshadow", "-Wall", cpp_file_path, "-o", "test", "-O2", "-Wno-unused-result"], capture_output=True, text=True)
    else:
        gcc_compile = subprocess.run(["g++", "-std=c++17", "-Wshadow", "-Wall", cpp_file_path, "-o", "test", "-g", "-fsanitize=address", "-fsanitize=undefined", "-D_GLIBCXX_DEBUG"], capture_output=True, text=True)

    print(Fore.BLUE + "----------------------------------------")
    if gcc_compile.returncode != 0:
        print("An Error Occurred During Compilation.")
        print("----------------------------------------")
        print(gcc_compile.stderr)
        print("----------------------------------------")
        return
    else:
        print("Compiled Successfully!")    
        print("----------------------------------------")
    

    testcases_path = path + "/testcases"
    all_testcases = os.listdir(testcases_path)
    all_testcases.reverse()
    
    for testcase in all_testcases:
        if "in" in testcase:
            input_file_path = testcases_path + "/" + testcase
            with open(input_file_path, 'r') as input_file:
                input_data = input_file.read()
                gcc_run = subprocess.run(["./test"], input=input_data, capture_output=True, text=True)

                if gcc_run.returncode != 0:
                    print(Fore.RED + "----------------------------------------")
                    print("RUN Error")
                    print("----------------------------------------")
                    print(gcc_run.stderr)
                    print("----------------------------------------")
                else:
                    output_file_path = testcases_path + "/" + testcase.replace("in","out")
                    with open(output_file_path, 'r') as output_file:
                        judge_output_data = output_file.read()
                        my_output_data = gcc_run.stdout
                        
                        with open(testcases_path+"/userOut",'w') as w:
                            w.writelines(my_output_data)

                        if judge_output_data == my_output_data:
                            print(Fore.GREEN + "----------------------------------------")
                            print("Accepted on Sample TestCase " + testcase.replace("in", "") + " !!")
                            print("----------------------------------------")
                        else:
                            print(Fore.RED + "----------------------------------------")
                            print("WrongAnswer on Sample TestCase " + testcase.replace("in", "") + " !!")
                            print("----------------------------------------")
                            print(Fore.BLUE + "Input")
                            print("----------------------------------------")
                            print(input_data)
                            print(Fore.GREEN + "----------------------------------------")
                            print("Judge Output")
                            print("----------------------------------------")
                            print(judge_output_data)
                            print("----------------------------------------")
                            print(Fore.YELLOW + "My Output")
                            print("----------------------------------------")
                            print(my_output_data)
                            print("----------------------------------------")

                            judge_output_data = judge_output_data.split('\n')
                            my_output_data = gcc_run.stdout.split('\n')
                            
                            for i in range(len(judge_output_data)):
                                if i > len(my_output_data) or judge_output_data[i] != my_output_data[i]:
                                    print(Fore.LIGHTMAGENTA_EX + "----------------------------------------")
                                    print("Output Doesn't Match in line :", i + 1)
                                    print(Fore.GREEN + "Judge Output: " + judge_output_data[i])
                                    print(Fore.RED + "My Output: " + (my_output_data[i] if i < len(my_output_data) else None))
                                    print(Fore.LIGHTMAGENTA_EX + "----------------------------------------")
                                    break
    os.remove("test")

