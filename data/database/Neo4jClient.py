from neo4j import GraphDatabase
import logging;

logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self, connection_uri):
        self._uri = connection_uri

    # Need to make the logger 
    def connect(self, username, password):
        try:
            AUTH = (username, password)
            driver = GraphDatabase.driver(self._uri, auth=AUTH)
            self._driver = driver
            
            logger.info("Neo4j Client Instantiated and waiting to verify connection ...")
            return driver
        except ConnectionError as e:
            logger.exception(f"Neo 4j client failed to connect with exception: {e}")

        def close(self):
            try:
                if self._driver.close() is None:
                    logger.error("Neo4j Client already does not exist")
                    assert "Neo4j Client already does not exist"
                self._driver.close()
                logger.info("Neo4j client channel closed successfully")
                
            except ConnectionError as e:
                logger.exception(f"Neo4j client failed to close the channel: {e}")
                