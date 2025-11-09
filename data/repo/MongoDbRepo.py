from .. import MongoDbClient
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class MongoDBRepo:
    def __init__(self, uri: str, port: int, db: str):

        try:
            self._client = MongoDbClient(uri, port)
            self._driver = self._client.connect()
            self._db = db
            logger.info(self._driver.server_info())
            logger.info("MongoDBRepo initialized and connection verified successfully.")
        except Exception as e:
            logger.exception(f"Failed to verify MongoDB connection: {e}")

    def add_collection(self, collection_name: str):
        """Create a new collection inside the database."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return

            
            db = self._driver.get_database(self._db)
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                logger.info(f"Collection '{collection_name}' created successfully.")
            else:
                logger.warning(f"Collection '{collection_name}' already exists.")
        except Exception as e:
            logger.exception(f"Failed to create collection '{collection_name}': {e}")

    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert a single document and return its ID."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return
            
            db = self._driver[self._db]
            result = db[collection_name].insert_one(document)
            logger.info(f"Inserted one document into '{collection_name}' with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.exception(f"Failed to insert document into '{collection_name}': {e}")
            return None

    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple documents and return their IDs."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return


            db = self._driver[self._db]
            result = db[collection_name].insert_many(documents)
            logger.info(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}'.")
            return [str(_id) for _id in result.inserted_ids]
        except Exception as e:
            logger.exception(f"Failed to insert documents into '{collection_name}': {e}")
            return []

    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document by query."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return


            db = self._driver[self._db]
            result = db[collection_name].find_one(query)
            logger.debug(f"find_one in '{collection_name}' with query {query} returned {result}")
            return result
        except Exception as e:
            logger.exception(f"Failed to find document in '{collection_name}': {e}")
            return None

    def find_many(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find multiple documents matching query."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return


            db = self._driver[self._db]
            results = list(db[collection_name].find(query))
            logger.debug(f"find_many in '{collection_name}' returned {len(results)} documents.")
            return results
        except Exception as e:
            logger.exception(f"Failed to find documents in '{collection_name}': {e}")
            return []

    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Update a single document and return number of modified documents."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return


            db = self._driver[self._db]
            result = db[collection_name].update_one(query, {'$set': update})
            logger.info(f"Updated {result.modified_count} document(s) in '{collection_name}'.")
            return result.modified_count
        except Exception as e:
            logger.exception(f"Failed to update document in '{collection_name}': {e}")
            return 0

    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete a single document and return count of deleted documents."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return


            db = self._driver[self._db]
            result = db[collection_name].delete_one(query)
            logger.info(f"Deleted {result.deleted_count} document(s) from '{collection_name}'.")
            return result.deleted_count
        except Exception as e:
            logger.exception(f"Failed to delete document from '{collection_name}': {e}")
            return 0

    def drop_collection(self, collection_name: str):
        """Drop a collection."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return


            db = self._driver[self._db]
            db.drop_collection(collection_name)
            logger.info(f"Collection '{collection_name}' dropped successfully.")
        except Exception as e:
            logger.exception(f"Failed to drop collection '{collection_name}': {e}")

    def list_collections(self) -> List[str]:
        """Return list of all collection names."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return


            db = self._driver[self._db]
            collections = db.list_collection_names()
            logger.debug(f"Collections in '{self._db}': {collections}")
            return collections
        except Exception as e:
            logger.exception(f"Failed to list collections: {e}")
            return []

    def close(self):
        """Close MongoDB client connection."""
        try:
            if '_driver' not in self.__dict__:
                logger.error("No MongoDB driver is created")
                assert RuntimeError("No MongoDB driver is created")
                return

            self._driver.close()
            logger.info("MongoDB connection closed.")
        except Exception as e:
            logger.exception(f"Failed to close MongoDB connection: {e}")
