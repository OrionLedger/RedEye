from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)

class MongoDbClient:
    def __init__(self, uri: str, port):
        self._uri = uri
        self._port = port

    def connect(self):
        try:
            client = MongoClient(self._uri, port = self._port)
            self._client = client
            
            logger.info("Mongo db client connected succesfully and is waiting for operations ...")
            return client
        
        except ConnectionError as e:
            logger.exception(f"Mongo db client failed to connect: {e}")
    
    def close(self):
        try:
            if self._client is None:
                logger.error("No Mongo DB client is created")
                assert "No Mongo DB client is created"
            self._client.close()

        except ConnectionError as e:
            logger.exception(f"Failed to close the connection: {e}")