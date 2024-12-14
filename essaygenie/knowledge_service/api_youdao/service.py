import os
import requests
from dotenv import load_dotenv
from typing import List, Optional, TypedDict

import essaygenie.utils as U
from example import load_json_example
from essaygenie.knowledge_service.api_youdao import auth_v3_util

load_dotenv()
        
class YoudaoService:
    """ 与网易有道智能云相关的服务 """
    
    def __init__(
        self,
        show_detail: bool = False,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None
        ):
        self.show_detail = show_detail
        self.app_key = app_key or os.getenv("YOUDAO_APP_KEY")
        self.app_secret = app_secret or os.getenv("YOUDAO_APP_SECRET")
        self.api_url = 'https://openapi.youdao.com/v2/correct_writing_text'
    
    
    def send_request(self, content: str, grade: str, title: str, model_content: str) -> dict:
        """ 网易有道智云英文作文批改服务api并返回响应 """
        data = {
            'q': content,
            'grade': grade,
            'to': title,
            'modelContent': model_content,
            'isNeedSynonyms': "true",
            'correctVersion': "basic"
        }
        
        auth_v3_util.add_auth_params(self.app_key,self.app_secret,data)
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(self.api_url, headers=headers, data=data)
            response.raise_for_status()  
            if self.show_detail:
                print(f"Youdao Request successful: {response.status_code}")
            return response.json()
        except requests.RequestException as e:
            if self.show_detail:
                print(f"Request failed: {e}")
            return None
        
    def send_request_dummpy(self) -> dict:
        """ 网易有道智云英文作文批改服务api并返回响应 """
        return U.load_json("essaygenie/knowledge_service/api_youdao/dummpy_response_basic.json")
