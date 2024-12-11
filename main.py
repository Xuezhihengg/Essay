from typing import List
from essaygenie.agents.grammar import GrammarAgent
from essaygenie.knowledge_service.api_youdao.service import YoudaoService
from essaygenie.knowledge_service.kg_neo4j.api import GrammarKnowledgeGraphAPI
from essaygenie.knowledge_service.kg_neo4j.connection_manager import Neo4jConnectionManager
from essaygenie.knowledge_service.kg_neo4j.service import GrammarKnowledgeGraphService


def neo4j_test():
    connection_manager = Neo4jConnectionManager() 
    service = GrammarKnowledgeGraphService(connection_manager)
    api = GrammarKnowledgeGraphAPI(service)
    results = api.get_node_neighbours("普通名词")
    print(results)

def grammar_agent_test():
    grammer_agent = GrammarAgent()
    
    youdao_service = YoudaoService()
    youdao_res = youdao_service.send_request_dummpy()
    
    parsed_youdao_res = grammer_agent.extract_error(youdao_res)
    
    for sentence_analysis_result in parsed_youdao_res:
        state = grammer_agent.init_state(sentence_analysis_result)
        while True:
            state = grammer_agent.determine_most_relevant(state)
            if state['searchDone']:
                break
            state = grammer_agent.get_neibor_nodes(state)
        
            
        
    

if __name__ == '__main__':
   grammar_agent_test()
        
       
    