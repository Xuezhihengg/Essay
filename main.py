import os
import requests
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("URL")

headers = {
    "Action": "ECC",  
    "Version": "2018-12-13",
}

data = {
    "Content": "value1",
    "key2": "value2"
}

try:
    response = requests.post(URL, headers=headers, json=data)

    if response.status_code == 200:
        print("请求成功:", response.json())
    else:
        print("请求失败:", response.status_code, response.text)
except requests.exceptions.RequestException as e:
    print("HTTP 请求发生错误:", str(e))
    