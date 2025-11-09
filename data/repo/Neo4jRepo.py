import logging
from .. import Neo4jClient
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class Neo4jRepo:
    def __init__(self, uri: str, username: str, password: str):
        """Initialize the Neo4j repository and establish a connection."""
        self._client = Neo4jClient(uri)
        self._driver = self._client.connect(username, password)
        logger.info("Neo4jRepo initialized successfully.")

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return the results as a list of dictionaries.
        Use this for read operations (MATCH, RETURN, etc.).
        """
        try:
            with self._driver.session() as session:
                result = session.run(query, parameters or {})
                data = [record.data() for record in result]
                logger.debug(f"Executed query: {query} with params: {parameters}, returned {len(data)} rows.")
                return data
        except Exception as e:
            logger.exception(f"Failed to execute query: {query}, error: {e}")
            return []

    def create_node(self, label: str, properties: Dict[str, Any]) -> bool:
        """
        Create a node with a given label and properties.
        Example: create_node("Person", {"name": "Alice", "age": 25})
        """
        try:
            query = f"CREATE (n:{label} $props)"
            with self._driver.session() as session:
                session.run(query, props=properties)
                logger.info(f"Node with label '{label}' created successfully.")
                return True
        except Exception as e:
            logger.exception(f"Failed to create node with label '{label}': {e}")
            return False

    def create_relationship(self, from_label: str, from_key: Dict[str, Any],
                            to_label: str, to_key: Dict[str, Any],
                            rel_type: str, rel_props: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create a relationship between two nodes.
        Example:
        create_relationship("Person", {"name": "Alice"}, "City", {"name": "London"}, "LIVES_IN")
        """
        try:
            rel_props = rel_props or {}
            query = (
                f"MATCH (a:{from_label} $from_key), (b:{to_label} $to_key) "
                f"CREATE (a)-[r:{rel_type} $rel_props]->(b)"
            )
            with self._driver.session() as session:
                session.run(query, from_key=from_key, to_key=to_key, rel_props=rel_props)
                logger.info(f"Relationship '{rel_type}' created between {from_label} and {to_label}.")
                return True
        except Exception as e:
            logger.exception(f"Failed to create relationship '{rel_type}': {e}")
            return False

    def find_nodes(self, label: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Find nodes by label and optional filters.
        Example: find_nodes("Person", {"name": "Alice"})
        """
        try:
            filters = filters or {}
            query = f"MATCH (n:{label} $filters) RETURN n"
            with self._driver.session() as session:
                result = session.run(query, filters=filters)
                data = [record["n"] for record in result]
                logger.debug(f"Found {len(data)} nodes with label '{label}' and filters {filters}.")
                return data
        except Exception as e:
            logger.exception(f"Failed to find nodes with label '{label}': {e}")
            return []

    def update_node(self, label: str, match_props: Dict[str, Any], update_props: Dict[str, Any]) -> int:
        """
        Update node properties based on a match filter.
        Example: update_node("Person", {"name": "Alice"}, {"age": 30})
        """
        try:
            query = f"MATCH (n:{label} $match_props) SET n += $update_props RETURN COUNT(n) AS count"
            with self._driver.session() as session:
                result = session.run(query, match_props=match_props, update_props=update_props)
                count = result.single()["count"]
                logger.info(f"Updated {count} node(s) with label '{label}'.")
                return count
        except Exception as e:
            logger.exception(f"Failed to update node with label '{label}': {e}")
            return 0

    def delete_node(self, label: str, match_props: Dict[str, Any]) -> int:
        """
        Delete nodes matching given properties.
        Example: delete_node("Person", {"name": "Alice"})
        """
        try:
            query = f"MATCH (n:{label} $match_props) DETACH DELETE n RETURN COUNT(n) AS count"
            with self._driver.session() as session:
                result = session.run(query, match_props=match_props)
                count = result.single()["count"]
                logger.info(f"Deleted {count} node(s) with label '{label}'.")
                return count
        except Exception as e:
            logger.exception(f"Failed to delete node with label '{label}': {e}")
            return 0

    def close(self):
        """Close the Neo4j driver connection."""
        try:
            if hasattr(self._driver, "close"):
                self._driver.close()
                logger.info("Neo4j driver closed successfully.")
        except Exception as e:
            logger.exception(f"Failed to close Neo4j driver: {e}")
