import os
import logging
import requests
from typing import Optional
from dotenv import load_dotenv

import essaygenie.utils as U
from essaygenie.knowledge_service.api_youdao import auth_v3_util

load_dotenv()
logger = logging.getLogger()

class YoudaoService:
    """ 与网易有道智能云相关的服务 """
    
    def __init__(
        self,
        app_key: Optional[str] = None,
        app_secret: Optional[str] = None
        ):
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
            'isNeedSynonyms': True,
            'correctVersion': "basic"
        }
        
        auth_v3_util.add_auth_params(data)
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(self.api_url, headers=headers, data=data)
            response.raise_for_status()  
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
        
    def send_request_dummpy(self) -> dict:
        """ 网易有道智云英文作文批改服务api并返回响应 """
        return U.load_json("essaygenie/knowledge_service/api_youdao/dummpy_response_basic.json")
        
    def extract_error(self, response: dict):
        """ 从网易有道智云英文作文批改服务api返回的响应中提取错误 """
        result = response.get('Result', {})
        essay_feedback = result.get('essayFeedback', {})
        sents_feedback = essay_feedback.get('sentsFeedback', [])
        
        error_infos = []
        
        for feedback in sents_feedback:
            # 每一句对应一个sentence_info
            sentence_info = {
                'rawSent': feedback.get('rawSent', ''), 
            }
        
            error_pos_infos = feedback.get('errorPosInfos', [])
            if error_pos_infos:
                #每一句都可能对应多个错误
                sentence_info['errorPosInfos'] = []
                for error_info in error_pos_infos:
                    sentence_info['errorPosInfos'].append({
                        'errorTypeTitle': error_info.get('errorTypeTitle', ''),
                        'orgChunk': error_info.get('orgChunk', ''),
                        'correctChunk': error_info.get('correctChunk', ''),
                        'errorBaseInfo': error_info.get('errorBaseInfo', ''),
                        'knowledgeExp': error_info.get('knowledgeExp', ''),
                        'exampleCases': error_info.get('exampleCases', []),
                        'isContainGrammarError': error_info.get('isContainGrammarError'),
                        'isContainTypoError': error_info.get('isContainTypoError'),
                        'isValidLangSent': error_info.get('isValidLangSent'),
                    })
                   
            error_infos.append(sentence_info) 
        return error_infos
            
                
        
if __name__ == '__main__':
    youdao_service = YoudaoService()
    youdao_res = youdao_service.send_request_dummpy()
    out = youdao_service.extract_error(youdao_res)
    print(out)
    