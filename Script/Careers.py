import requests
from bs4 import BeautifulSoup
import json
import functools 
import math
import collections
collections.Callable = collections.abc.Callable
from colorama import Fore

import asyncio
import aiofiles as aiof


async def get_salary():
    salary_url = "https://tahanima.github.io/2021/09/12/monetary-compensation-at-various-software-companies-of-bangladesh-for-an-entry-level-position/"
    salary_res = requests.get(salary_url)
    salary_bts = BeautifulSoup(salary_res.text, 'lxml')

    all_companies = salary_bts.find("tbody").find_all("tr")
    software_company_details_bd = dict()

    for company in all_companies:
        data = [x.text.strip() for x in company.find_all('td')]
        salary = [x.strip() for x in ((data[2].replace('Tk.', '')).replace(',', '')).strip().split(' ') if x != "" and x != "-"]
        
        if data[0] in software_company_details_bd:
            software_company_details_bd[data[0]]['Positions'].append(
                {
                    'Position' : data[1],
                    'Salary' : {
                        'Low' : int(salary[0]),
                        'Hi' : int(salary[1])
                    }
                }
            )
        else:
            software_company_details_bd[data[0]] = {
                "Name" : data[0],
                "Positions" : [
                    {
                        'Position' : data[1],
                        'Salary' : {
                            'Low' : int(salary[0]),
                            'Hi' : int(salary[1])
                        }
                    }
                ]
            }
    return software_company_details_bd

async def get_profile():
    company_profile_url = "https://tahanima.github.io/2022/04/01/profile-of-software-companies-of-bd/"
    company_profile_res = requests.get(company_profile_url)
    company_profile_bts = BeautifulSoup(company_profile_res.text, 'lxml')

    all_companies_info = company_profile_bts.find("table").find_all("tr")
    company_profile = list()

    for company in all_companies_info:
        data = company.find_all('td')
        if len(data) == 5:
            name = data[0].text.strip()
            website = data[1].find('a')['href']
            career_website = "".join([x['href'].strip() for x in data[2].find_all('a') if x['href'].strip() != ""])
            facebook = "".join([x['href'].strip() for x in data[3].find_all('a') if x['href'].strip() != ""])
            linkedin = "".join([x['href'].strip() for x in data[4].find_all('a') if x['href'].strip() != ""])
            company_profile.append({
                'Name' : name,
                'Website' : website,
                'Career' : career_website,
                'Facebook': facebook,
                'LinkedIn' : linkedin
            })
    return company_profile

async def get_details():
    try:
        software_company_details_bd = asyncio.create_task(get_salary())
        company_profile = asyncio.create_task(get_profile())
        software_company_details_bd = await software_company_details_bd
        company_profile = await company_profile
        
        for company in company_profile:
            name = ' '.join([x.strip().replace('.', '').lower() for x in company['Name'].split() if x.strip().replace('.', '').lower() != 'ltd'])
            matched_company = ""
            for company_name, data in software_company_details_bd.items():
                if name.replace('limited', '').strip() in ' '.join([x.strip() for x in company_name.lower().split('.') if x.strip() != ""]):
                    matched_company = company_name
            if matched_company == "":
                software_company_details_bd[company['Name']] = company
            else:
                software_company_details_bd[matched_company]['Website'] = company['Website']
                software_company_details_bd[matched_company]['Career'] = company['Career']
                software_company_details_bd[matched_company]['Facebook'] = company['Facebook']
                software_company_details_bd[matched_company]['LinkedIn'] = company['LinkedIn']
        return {
            'Response' : 'ok',
            'Companies' : software_company_details_bd
        }
    except:
        return {
            "Response" : "error"
        }

async def render_data(data, search_key):
    sorted_data = list()
    if data['Response'] == 'ok':
        for name, data in data['Companies'].items():
            lo = 1000000000
            hi = 0
            if 'Positions' in data:
                for Position in data['Positions']:
                    lo = min(lo, Position['Salary']['Low'])
                    hi = max(hi, Position['Salary']['Hi'])
            if lo == 1000000000:
                lo = 0
            if search_key.lower() in data['Name'].lower():
                sorted_data.append((lo, hi, data))
        sorted_data = sorted(sorted_data, key = lambda x: (-x[1], -x[0]))

        flg = True
        for data in sorted_data:
            print((Fore.GREEN if flg else Fore.RED) + "------------------------------")
            print("Name: " + Fore.MAGENTA + data[2]['Name'])
            print((Fore.GREEN if flg else Fore.RED), end='')
            
            if 'Positions' in data[2]:
                for p in data[2]['Positions']:
                    print((Fore.GREEN if flg else Fore.RED), end='')
                    print(p['Position'] + " | Salary: " + Fore.BLUE + str(p['Salary']['Low']) + " - " + str(p['Salary']['Hi']))

            print((Fore.GREEN if flg else Fore.RED), end='')
            if 'Website' in data[2] and data[2]['Website'] != "":
                print("Website: " + data[2]['Website'])
            if "Career" in data[2] and data[2]['Career'] != "":
                print("Career: " + data[2]['Career'])
            if 'Facebook' in data[2] and data[2]['Facebook'] != "":
                print("Facebook: " + data[2]['Facebook'])
            if 'LinkedIn' in data[2] and data[2]['LinkedIn'] != "":
                print("LinkedIn: " + data[2]['LinkedIn'])
            print("------------------------------")
            flg = not flg
        if len(sorted_data) == 0:
            print(Fore.GREEN + "------------------------------")           
            print(Fore.RED + "No Match Found")
            print(Fore.BLUE + "You can keep the company name empty for getting all companies data.")
            print(Fore.GREEN + "------------------------------")           
    else:
        print(Fore.YELLOW + "--------------------------------------")
        print(Fore.RED + "Error occered, please try again.")
        print(Fore.YELLOW + "--------------------------------------")

async def GetCareerData(search_key):
    data = await asyncio.create_task(get_details())
    await asyncio.create_task(render_data(data, search_key))

if __name__ == '__main__':
    GetCareerData("")

