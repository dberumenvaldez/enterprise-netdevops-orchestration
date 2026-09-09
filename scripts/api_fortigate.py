import requests
import os
from dotenv import load_dotenv

# Search for tokens
load_dotenv()

FORTIGATE_IP = "10.10.10.1"
TOKEN = os.getenv("FORTIGATE_TOKEN")

headers = {
    "Authorization":f"Bearer {TOKEN}",
}

url = f"http://{FORTIGATE_IP}/api/v2/cmdb/system/interface"


try:
    print("[*] Try GET on API REST by FortiOS...")

    response = requests.get(url,headers=headers,verify=False)
    response.raise_for_status()

    data = response.json()

    for interface in data.get("results",[]):
        name = interface.get("name")
        ip = interface.get("ip","No IP address")
        status = "UP" if interface.get("status")=="up" else "DOWN"

        print(f"[{status}] interface: {name.ljust(12)} | address: {ip}")
    
except Exception as e:
    print(f"[ERROR] Http request fails: {e}")
