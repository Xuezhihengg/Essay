from typing import List, TypedDict

from .service import GrammarKnowledgeGraphService


class GrammarKnowledgeGraphAPI:
    """知识图查询的API封装"""
    
    class NodeDetail(TypedDict):
        description: str
        examples: List[str]

    def __init__(self, service: GrammarKnowledgeGraphService):
        self.service = service

    def get_top_grammar_concepts(self) -> List[str]:
        return self.service.get_top_grammar_concepts()

    def get_node_neighbours(self, node_id: str) -> List[str]:
        return self.service.get_node_neighbours(node_id)

    def get_node_labels(self, node_id: str) -> List[str]:
        return self.service.get_node_labels(node_id)

    def get_node_detail(self, node_id: str) -> NodeDetail:
        description = self.service.get_node_description(node_id)
        examples = self.service.get_node_examples(node_id)
        return {"description": description, "examples": examples}
