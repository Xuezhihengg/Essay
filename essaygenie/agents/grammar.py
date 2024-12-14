from typing import List, Optional, TypedDict

import jieba
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from essaygenie.prompts import load_prompt_from_folder
from essaygenie.knowledge_service.kg_neo4j.api import GrammarKnowledgeGraphAPI
from essaygenie.knowledge_service.kg_neo4j.service import GrammarKnowledgeGraphService
from essaygenie.knowledge_service.kg_neo4j.connection_manager import Neo4jConnectionManager

class ExampleCase(TypedDict):
    right: str
    rightTranslate: str
    error: str

class ErrorPosInfo(TypedDict):
    errorId: int
    startPos: int
    endPos: int
    errorTypeTitle: str
    orgChunk: str
    correctChunk: str
    errBaseInfo: Optional[str]
    knowledgeExp: Optional[str]
    exampleCases: List[ExampleCase]
    candidate_nodes: List[str] = []
    gc_nodes: List[str] = []
    rule_nodes: List[str] = []
    llm_analysis: str = ""
    
class SentGrammarErrors(TypedDict):
    rawSent: str
    correctedSent: str
    paraId: int
    sentId: int
    sentStartPos: int
    errorPosInfos: List[ErrorPosInfo]
    sentFeedback: str
    isContainGrammarError: bool
    isValidLangSent: bool
    searchDone: bool = False
    

class GrammarAgent:
    def __init__(
        self,
        model_name = 'ERNIE-4.0',
        temperature = 0.8,
        request_timout = 120,
        show_detail = False,
        llm_max_retries = 3
        ) -> None:
        connection_manager = Neo4jConnectionManager() 
        grammar_kg_service = GrammarKnowledgeGraphService(connection_manager)
        self.grammar_kg_api = GrammarKnowledgeGraphAPI(grammar_kg_service)
        self.show_detail = show_detail
        self.llm_max_retries = llm_max_retries
        
        self.llm = QianfanLLMEndpoint(
            model_name=model_name,
            temperature=temperature,
            request_timout=request_timout)
        
        
    def extract_error(self, response: dict) -> List[SentGrammarErrors]:
        """从网易有道智云英文作文批改服务api返回的响应中提取错误信息"""
        result = response.get('Result', {})
        essay_feedback = result.get('essayFeedback', {})
        sents_feedback = essay_feedback.get('sentsFeedback', [])
        
        error_infos = []
        # sents_feedback表示整个文章的反馈，每个元素feedback是一句话的反馈
        for feedback in sents_feedback:
            sentence_info: SentGrammarErrors = {
                'rawSent': feedback.get('rawSent'), 
                'correctedSent': feedback.get('correctedSent'),
                'paraId': feedback.get('paraId'),
                'sentId': feedback.get('sentId'),
                'sentStartPos': feedback.get('sentStartPos'),
                'sentFeedback': feedback.get('sentFeedback'),
                'isContainGrammarError': feedback.get('isContainGrammarError'),
                'isValidLangSent': feedback.get('isValidLangSent'),
                'searchDone': False,
            }
            
            if sentence_info['isContainGrammarError'] == False or sentence_info['isValidLangSent'] == False:
                continue
    
            error_pos_infos = feedback.get('errorPosInfos', [])
            if error_pos_infos:
                # errorPosInfos表示一句话的错误信息，每个元素error_info是该句话中一处错误的信息
                sentence_info['errorPosInfos'] = []
                for error_info in error_pos_infos:
                    sentence_info['errorPosInfos'].append({
                        'errorId': error_info.get('id'),
                        'startPos': error_info.get('startPos'),
                        'endPos': error_info.get('endPos'),
                        'errorTypeTitle': error_info.get('errorTypeTitle'),
                        'orgChunk': error_info.get('orgChunk'),
                        'correctChunk': error_info.get('correctChunk'),
                        'errBaseInfo': error_info.get('errBaseInfo'),
                        'knowledgeExp': error_info.get('knowledgeExp'),
                        'exampleCases': error_info.get('exampleCases'),
                        'candidate_nodes': [],
                        'gc_nodes': [],
                        'rule_nodes': [],
                        'llm_analysis': ""
                    })                
            error_infos.append(sentence_info) 
        return error_infos


    def init_state(self, state: SentGrammarErrors) -> SentGrammarErrors:
        """初始化语法概念节点"""
        top_nodes = self.grammar_kg_api.get_top_grammar_concepts()
        assert isinstance(top_nodes, list) and len(top_nodes) > 0
        
        for error_pos_info in state["errorPosInfos"]:
            error_pos_info['candidate_nodes'] = top_nodes
        
        if self.show_detail:
            print("GrammarAgent.init_nodes: State initialized") 
        return state
        
    
    def determine_most_relevant(self, state: SentGrammarErrors) -> SentGrammarErrors:
        """从若干语法概念中，与输入语法解析最相关的概念"""
        done_counter = 0
        for error_pos_info in state['errorPosInfos']:
            # 如果已搜索完全部的GrammarConcept节点，则跳过
            if len(error_pos_info['gc_nodes']) == 0:
                done_counter += 1
                continue
            
            candidate_nodes = error_pos_info['candidate_nodes']
            error_type_title = error_pos_info['errorTypeTitle']
            error_base_info = error_pos_info['errBaseInfo']
            target_str = f'{error_type_title}:{error_base_info}'
            
            # FIXME: 这里到底需不需要使用相似度搜索尚未确定
            # relevant_nodes = self.similarity_search(target_str, candidate_nodes)
            
            relevant_nodes = []
            # 若没有找到相关节点，则使用LLM判断
            if relevant_nodes == []:
                if self.show_detail:
                    print(f"GrammarAgent.determine_most_relevant: No relevant nodes found for error type: {error_type_title}-{error_base_info}, using LLM to determine")
               
                relevant_nodes = self.determine_most_relevant_by_llm(
                    raw_sent=state['rawSent'],
                    error=target_str,
                    nodes=candidate_nodes,
                    max_retries=self.llm_max_retries
                )
            if self.show_detail:
                print(f"GrammarAgent.determine_most_relevant: Relevant nodes found for error type: {error_type_title}: {relevant_nodes}")
           
            # 更新error_pos_infos中的gc_nodes和rule_nodes
            error_pos_info['gc_nodes'] = []
            for node in relevant_nodes:
                node_labels = self.grammar_kg_api.get_node_labels(node)
                if "GrammarConcept" in node_labels:
                    error_pos_info['gc_nodes'].append(node)
                elif "Rule" in node_labels:
                    error_pos_info['rule_nodes'].append(node)
            
        if done_counter == len(state['errorPosInfos']):
            if self.show_detail:
                print(f"GrammarAgent.determine_most_relevant: All relevant nodes found")
            state['searchDone'] = True
        return state


    def determine_most_relevant_by_llm(self, raw_sent: str, error: str, nodes: List[str], max_retries: int) -> List[str]:
        """使用LLM判断若干语法概念中，与输入语法解析最相关的概念"""
        if max_retries == 0:
            if self.show_detail:
                print(f"GrammarAgent.determine_most_relevant_by_llm: Max retries reached")
            raise RuntimeError("GrammarAgent.determine_most_relevant_by_llm: Max retries reached")
        
        assert isinstance(raw_sent, str)
        assert isinstance(error, str)
        assert isinstance(nodes, list) and len(nodes) > 0
        
        system_template = load_prompt_from_folder("grammar", "determine_most_relevant")
        system_message_prompt = PromptTemplate.from_template(
            template=system_template,
        )
        parser = JsonOutputParser()
        chain = system_message_prompt | self.llm | parser
        
        try:
            llm_output = chain.invoke({
                "rawSent": raw_sent,
                "error": error,
                "nodes": nodes
            })
        
            assert isinstance(llm_output, list) and len(llm_output) > 0
            return llm_output
        
        except Exception as e:
            if self.show_detail:
                print(f"GrammarAgent.determine_most_relevant_by_llm: Error: {e}")
            
            return self.determine_most_relevant_by_llm(
                raw_sent=raw_sent,
                error=error,
                nodes=nodes,
                max_retries=max_retries - 1,
            )
        

    def similarity_search(self, target_str: str, str_list: List[str], top_n: int = 1) -> List[str]:
        """在字符串列表中搜索与目标字符串F1得分最高的前top_n个字符串"""
        def f1_score(set1: set, set2: set) -> float:
            """计算两个集合的F1得分"""
            common = set1 & set2
            if not common:
                return 0.0
            precision = len(common) / len(set1)
            recall = len(common) / len(set2)
            return 2 * (precision * recall) / (precision + recall)
        
        target_words = set(jieba.cut(target_str))
        scored_strs = []
        
        for s in str_list:
            s_words = set(jieba.cut(s))
            score = f1_score(target_words, s_words)
            scored_strs.append((s, score))
        
        # 按照得分从高到低排序，并取前top_n个
        scored_strs.sort(key=lambda x: x[1], reverse=True)
        top_matches = [s for s, score in scored_strs[:top_n]]
        
        return top_matches
    
    def cosine_similarity_search(target_str: str, str_list: List[str], top_n: int = 3) -> List[str]:
        """在字符串列表中搜索与目标字符串余弦相似度最高的前 top_n 个字符串"""
        vectorizer = TfidfVectorizer().fit([target_str] + str_list)
        vectors = vectorizer.transform([target_str] + str_list)

        target_vector = vectors[0]  
        str_vectors = vectors[1:]   
        
        similarities = cosine_similarity(target_vector, str_vectors).flatten()
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        top_matches = [str_list[i] for i in top_indices]
        
        return top_matches

    
    
    def get_neibor_nodes(self, state: SentGrammarErrors) -> SentGrammarErrors:
        """获取语法概念节点的邻居节点"""
        for error_pos_infos in state['errorPosInfos']:
            gc_nodes = error_pos_infos['gc_nodes']
            neibor_nodes = []
            for node in gc_nodes:
                neighbours = self.grammar_kg_api.get_node_neighbours(node)
                neibor_nodes.extend(neighbours)
            error_pos_infos['candidate_nodes'] = neibor_nodes
        return state
    
    
    def generate_analysis(self,state: SentGrammarErrors) -> SentGrammarErrors:
        """生成语法错误分析"""
        raw_sent = state['rawSent']
        for error_pos_info in state['errorPosInfos']:
            error = ''.join([error_pos_info['errorTypeTitle'], ':', error_pos_info['errBaseInfo']])
            knowledge = error_pos_info['knowledgeExp'] or ""
            rule_nodes = error_pos_info['rule_nodes']
            for rule_node in rule_nodes:
                detail = self.grammar_kg_api.get_node_detail(rule_node)
                knowledge += (' && ' + detail['description'])
                
            llm_analysis = self.generate_analysis_by_llm(
                raw_sent=raw_sent,
                error=error,
                knowledge=knowledge,
                max_retries=self.llm_max_retries
            )
            
            if self.show_detail:
                print(f"GrammarAgent.generate_analysis: LLM analysis generated for error '{error}': {llm_analysis}")
            error_pos_info['llm_analysis'] = llm_analysis
        
        return state
               
          
    def generate_analysis_by_llm(self, raw_sent: str, error: str, knowledge: str,max_retries: int) -> str:
        
        if max_retries == 0:
            if self.show_detail:
                print(f"GrammarAgent.determine_most_relevant_by_llm: Max retries reached")
            raise RuntimeError("GrammarAgent.determine_most_relevant_by_llm: Max retries reached")
        
        system_template = load_prompt_from_folder("grammar", "generate_analysis")
        system_message_prompt = PromptTemplate.from_template(
                template=system_template,
            )
        parser = StrOutputParser()
        chain = system_message_prompt | self.llm | parser
            
        try:
            llm_output = chain.invoke({
                "rawSent": raw_sent,
                "error": error,
                "knowledge": knowledge
            })
            
            assert isinstance(llm_output, str)
            return llm_output
        except Exception as e:
            if self.show_detail:
                print(f"GrammarAgent.determine_most_relevant_by_llm: Retrying... remaining number of retryes: {max_retries}")
            
            return self.generate_analysis_by_llm(
                raw_sent=raw_sent,
                error=error,
                knowledge=knowledge,
                max_retries=max_retries - 1,
            )
            
        
    
               
            
               
               
               
            
        
        
