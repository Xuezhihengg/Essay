from typing import List, TypedDict

from langchain.prompts import SystemMessagePromptTemplate
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint

from essaygenie.prompts import load_prompt_from_folder
from essaygenie.knowledge_service import *
from essaygenie.knowledge_service.kg_neo4j.api import GrammarKnowledgeGraphAPI
from essaygenie.knowledge_service.kg_neo4j.service import GrammarKnowledgeGraphService
from essaygenie.knowledge_service.kg_neo4j.connection_manager import Neo4jConnectionManager
from essaygenie.knowledge_service.api_youdao.service import ExampleCase, ErrorPosInfo, SentenceAnalysisResult

class GrammarState(TypedDict):
    sentence_info: SentenceAnalysisResult
    grammar_nodes: List[str]
    

class GrammarAgent:
    def __init__(
        self,
        model_name = 'ERNIE-4.0-Turbo-128K',
        temperature = 0,
        request_timout=120) -> None:
        
        connection_manager = Neo4jConnectionManager() 
        grammar_kg_service = GrammarKnowledgeGraphService(connection_manager)
        self.grammar_kg_api = GrammarKnowledgeGraphAPI(grammar_kg_service)
        
        
        self.llm = QianfanLLMEndpoint(
            model_name=model_name,
            temperature=temperature,
            request_timout=request_timout)
        
    # def determine_top_gc(self, sentence: str) -> None:
    
    #     top_grammar_concepts = self.grammar_kg_api.get_top_grammar_concepts()

    #     prompt = load_prompt("grammar_determine_top_gc")


    #     prompt = PromptTemplate.from_template(
    #         template=prompt_template,
    #         partial_variables={"format_instructions": parser.get_format_instructions()}
    #     )

    #     # prompt_retry = PromptTemplate.from_template(
    #     #     template=prompt_template_retry,
    #     #     partial_variables={"format_instructions": parser_retry.get_format_instructions()}
    #     # )
    #     chain = prompt | model | parser
    #     # chain_retry = prompt_retry | model | parser_retry

    #     output = chain.invoke({"sentence": state["sentence"], "concepts": top_gc_nodes})

    #     # output = output.answer
    #     # for item in output:
    #     #     for concept in item["concepts"]:
    #     #         if concept not in top_gc_nodes:
    #     #             item["concepts"].remove(concept)

    #         # if len(item["concepts"]) == 0:
    #             # item = chain_retry.invoke({"error": item})

    #     print("-" * 50 + "determine_top_gc" + "-" * 50)
    #     print(output)

    #     return output
    

        
        
    
    # def determine_most_relevant(state: GrammarState) -> None:
    #     """
    #     使用LLM判断若干语法概念中，与输入语法解析最相关的概念
    #     :param state: 一个AnalysisState对象，来自get_neighbours将但语法概念拓展后
    #     :return: 最相关分析后的AnalysisState对象
    #     """
        
    #     system_template = load_prompt_from_folder("grammar", "determine_most_relevant")
        
    #     system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        
    #     system_message = system_message_prompt.format_message()
    #     # assert isinstance(system_message, SystemMessage)
            
        
        

        
        

    #     chain = model

    #     for item in state:
    #         if item["isRule"]:
    #             continue

    #         output = chain.invoke({"analysis": item["analysis"], "concepts": item["concepts"]})
    #         item["concepts"] = [output.concept]

    #     print("-" * 50 + "determine_most_relevant" + "-" * 50)
    #     print(state)

    #     return AnalysisState(answer=state)
    
