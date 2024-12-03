# kg refers to the knowledge graph

from .connection_manager import Neo4jConnectionManager
from .service import GrammarKnowledgeGraphService
from .api import GrammarKnowledgeGraphAPI

# # use-case
# connection_manager = Neo4jConnectionManager() 
# service = GrammarKnowledgeGraphService(connection_manager)
# api = GrammarKnowledgeGraphAPI(service)
# results = api.get_top_grammar_concepts()
