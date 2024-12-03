from typing import Dict, List
from neo4j.exceptions import Neo4jError

from .connection_manager import Neo4jConnectionManager

class GrammarKnowledgeGraphService:
    """与语法知识图相关的查询服务"""

    def __init__(self, connection_manager: Neo4jConnectionManager):
        self.connection_manager = connection_manager

    def execute_query(self, query: str, parameters: Dict = None) -> List[Dict]:
        """执行Neo4j查询"""
        parameters = parameters or {}
        with self.connection_manager.get_session() as session:
            try:
                result = session.run(query, **parameters)
                return result.data()
            except Neo4jError as e:
                raise RuntimeError(f"Query execution failed: {e}")

    def get_top_grammar_concepts(self) -> List[str]:
        """获取所有顶级语法概念节点的ID"""
        query = """
        MATCH (n:GrammarConcept)
        WHERE n.type = 'top'
        RETURN n.id AS id
        """
        results = self.execute_query(query)
        return [record["id"] for record in results]

    def get_node_neighbours(self, node_id: str) -> List[str]:
        """获取指定节点的所有邻居节点ID"""
        query = """
        MATCH (n {id: $node_id})-[:BELONGS_TO|HAS_SUBCLASS]->(neighbour)
        RETURN neighbour.id AS id
        """
        results = self.execute_query(query, {"node_id": node_id})
        return [record["id"] for record in results]

    def get_node_labels(self, node_id: str) -> List[str]:
        """获取指定节点的所有标签"""
        query = """
        MATCH (n {id: $node_id})
        RETURN labels(n) AS labels
        """
        results = self.execute_query(query, {"node_id": node_id})
        return results[0]["labels"] if results else []

    def get_node_description(self, node_id: str) -> str:
        """获取指定节点的描述"""
        query = """
        MATCH (n {id: $node_id})
        RETURN n.description AS description
        """
        results = self.execute_query(query, {"node_id": node_id})
        return results[0]["description"] if results else ""

    def get_node_examples(self, node_id: str) -> List[str]:
        """获取指定节点关联的示例"""
        query = """
        MATCH (n {id: $node_id})-[:HAS_EXAMPLE]->(example)
        RETURN example.example AS example
        """
        results = self.execute_query(query, {"node_id": node_id})
        return [record["example"] for record in results]