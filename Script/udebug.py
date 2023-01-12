from urllib import response
import requests
import json

def main():
    url = "https://www.udebug.com/input_api/input_list/retrieve.json?judge_alias=UVa&problem_id=100"
    response = requests.get(url, auth=("ShouravAhmed", "WaterLily@898"))
    print(response.content)


if __name__ == "__main__":
    main()