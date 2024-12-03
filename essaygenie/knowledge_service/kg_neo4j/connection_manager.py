import os
import dotenv
from typing import Optional
from neo4j.exceptions import Neo4jError
from neo4j import GraphDatabase, Neo4jDriver, Session

dotenv.load_dotenv()

class Neo4jConnectionManager:
    """管理与Neo4j数据库的连接"""

    def __init__(self, 
                 uri: Optional[str] = None, 
                 username: Optional[str] = None, 
                 password: Optional[str] = None, 
                 database: Optional[str] = None):
    
        self.uri = uri or os.getenv("NEO4J_URI")
        self.username = username or os.getenv("NEO4J_USERNAME")
        self.password = password or os.getenv("NEO4J_PASSWORD")
        self.database = database or os.getenv("NEO4J_DATABASE")

        if not all([self.uri, self.username, self.password]):
            raise ValueError("Neo4j connection details must be provided either as arguments or environment variables.")
        
        self.driver: Optional[Neo4jDriver] = None
        self.connect()

    def connect(self):
        """初始化数据库连接"""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        except Neo4jError as e:
            raise ConnectionError(f"Failed to connect to Neo4j: {e}")

    def close(self):
        """关闭数据库连接"""
        if self.driver:
            self.driver.close()

    def get_session(self) -> Session:
        """获取一个新的数据库会话"""
        if not self.driver:
            raise ConnectionError("No active Neo4j connection.")
        return self.driver.session(database=self.database)

