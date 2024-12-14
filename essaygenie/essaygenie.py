from typing import List, TypedDict
from essaygenie.agents.grammar import GrammarAgent, SentGrammarErrors
from essaygenie.knowledge_service.api_youdao.service import YoudaoService

class Essay(TypedDict):
    content: str
    grade: str
    title: str
    model_content: str

class EssayGenie:
    def __init__(
        self,
        grammar_agent_model_name: str = 'ERNIE-4.0',
        grammar_agent_temperature: str = 0.8,
        grammar_agent_show_detail: bool = False,
        grammar_agent_llm_max_retries: int = 3,
        ):
        """
        :param grammar_agent_model_name: GrammarAgent所使用的模型
        :param grammar_agent_temperature: GrammarAgent的模型temperature
        :param grammar_agent_show_detail: GrammarAgent是否展示详细信息
        :param grammar_agent_llm_max_retries: GrammarAgent中模型的最大重试次数
        """
        self.grammar_agent = GrammarAgent(
            model_name=grammar_agent_model_name,
            temperature=grammar_agent_temperature,
            show_detail=grammar_agent_show_detail,
            llm_max_retries=grammar_agent_llm_max_retries
        )
        self.youdao_service = YoudaoService()
        

    def correct_essay(self, essay: Essay) -> List[SentGrammarErrors]:
        youdao_res = self.youdao_service.send_request(
            content=essay['content'],
            grade=essay['grade'],
            title=essay['title'],
            model_content=essay['model_content']
        )
        
        parsed_youdao_res = self.grammar_agent.extract_error(youdao_res)
        
        essay_result: List[SentGrammarErrors] = []
        for sentence_analysis_result in parsed_youdao_res:
            state = self.grammar_agent.init_state(sentence_analysis_result)
            while True:
                state = self.grammar_agent.determine_most_relevant(state)
                if state['searchDone']:
                    break
                state = self.grammar_agent.get_neibor_nodes(state)
            
            state = self.grammar_agent.generate_analysis(state)
            essay_result.append(state)
            
        return essay_result
    
    
        
essay_genie = EssayGenie()   
        
        