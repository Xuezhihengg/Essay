from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint

class SynonymAgent:
    def __init__(
        self,
        model_name = 'ERNIE-4.0',
        temperature = 0.8,
        request_timout = 120,
        show_detail = False,
        llm_max_retries = 3
        ) -> None:    
        self.show_detail = show_detail
        self.llm_max_retries = llm_max_retries
        
        self.llm = QianfanLLMEndpoint(
            model_name=model_name,
            temperature=temperature,
            request_timout=request_timout)
        
    