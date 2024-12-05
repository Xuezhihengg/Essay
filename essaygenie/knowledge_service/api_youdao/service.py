import os
import logging
import requests
from dotenv import load_dotenv
from typing import List, Optional, TypedDict

import essaygenie.utils as U
from example import load_json_example
from essaygenie.knowledge_service.api_youdao import auth_v3_util

load_dotenv()
logger = logging.getLogger()

class ExampleCase(TypedDict):
    right: str
    rightTranslate: str
    error: str

class ErrorPosInfo(TypedDict):
    errorTypeTitle: str
    orgChunk: str
    correctChunk: str
    errorBaseInfo: Optional[str]
    knowledgeExp: Optional[str]
    exampleCases: List[ExampleCase]

class SentenceAnalysisResult(TypedDict):
    rawSent: str
    errorPosInfos: List[ErrorPosInfo]
    isContainGrammarError: bool
    isContainTypoError: bool
    isValidLangSent: bool
        
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
            'isNeedSynonyms': "true",
            'correctVersion': "basic"
        }
        
        auth_v3_util.add_auth_params(self.app_key,self.app_secret,data)
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(self.api_url, headers=headers, data=data)
            response.raise_for_status()  
            logger.info(f"Youdao Request successful: {response.status_code}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
        
    def send_request_dummpy(self) -> dict:
        """ 网易有道智云英文作文批改服务api并返回响应 """
        return U.load_json("essaygenie/knowledge_service/api_youdao/dummpy_response_basic.json")
        
    def extract_error(self, response: dict) -> List[SentenceAnalysisResult]:
        """ 从网易有道智云英文作文批改服务api返回的响应中提取错误 """
        result = response.get('Result', {})
        essay_feedback = result.get('essayFeedback', {})
        sents_feedback = essay_feedback.get('sentsFeedback', [])
        
        error_infos = []
        # sents_feedback表示整个文章的反馈，每个元素feedback是一句话的反馈
        for feedback in sents_feedback:
            sentence_info = {
                'rawSent': feedback.get('rawSent', ''), 
            }
        
            error_pos_infos = feedback.get('errorPosInfos', [])
            if error_pos_infos:
                # errorPosInfos表示一句话的错误信息，每个元素error_info是该句话中一处错误的信息
                sentence_info['errorPosInfos'] = []
                for error_info in error_pos_infos:
                    sentence_info['errorPosInfos'].append({
                        'errorTypeTitle': error_info.get('errorTypeTitle', ''),
                        'orgChunk': error_info.get('orgChunk', ''),
                        'correctChunk': error_info.get('correctChunk', ''),
                        'errorBaseInfo': error_info.get('errorBaseInfo', ''),
                        'knowledgeExp': error_info.get('knowledgeExp', ''),
                        'exampleCases': error_info.get('exampleCases', []),
                    })
                sentence_info.update({
                    'isContainGrammarError': feedback.get('isContainGrammarError'),
                    'isContainTypoError': feedback.get('isContainTypoError'),
                    'isValidLangSent': feedback.get('isValidLangSent'),
                })
                
            error_infos.append(sentence_info) 
        return error_infos
            
                
        
if __name__ == '__main__':
    example = load_json_example("example01.json")
    content = example['Content']
    grade = example['Grade']
    title = example['Title']
    model_content = example['ModelContent']
    
    youdao_service = YoudaoService()
    youdao_res = youdao_service.send_request(
        content=content,
        grade=grade,
        title=title,
        model_content=model_content
    )
    out = youdao_service.extract_error(youdao_res)
    print(out)
    
