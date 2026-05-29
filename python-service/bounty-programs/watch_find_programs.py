import requests, os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import insert_all_bugcrowd_programs

URL = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/bugcrowd_data.json"

def RunCode():
    try:
        response = requests.get(URL, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        insert_all_bugcrowd_programs(data)
        
        return data
    except requests.RequestException as e:
        print("error:", e)
        return None

if __name__ == '__main__':
    RunCode()