from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)

class MongoDbClient:
    def __init__(self, uri: str, port:int):
        self._uri = uri
        self._port = port

    def connect(self):
        try:
            driver = MongoClient(self._uri, port = self._port)
            self._driver = driver
            
            logger.info("Mongo db driver Instantiated succesfully and is waiting to verify Connection ...")
            return driver
        
        except ConnectionError as e:
            logger.exception(f"Mongo db driver failed to Instantiate: {e}")
    
    def close(self):
        try:
            if self._driver is None:
                logger.error("No Mongo DB driver is created")
                assert "No Mongo DB driver is created"
            self._driver.close()

        except ConnectionError as e:
            logger.exception(f"Failed to close the connection: {e}")