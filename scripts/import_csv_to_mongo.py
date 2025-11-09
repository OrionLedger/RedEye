import argparse
import csv
import logging
from data.repo.MongoDbRepo import MongoDBRepo  # adjust import path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Map relation types to document fields
RELATION_MAP = {
    "event": "events",
    "friend": "friends",
    "group": "groups",
    "neighbor": "neighbors"
}

def import_lastfm_file(repo: MongoDBRepo, input_file: str, collection_name: str = "users"):
    try:
        repo.add_collection(collection_name)

        count = 0
        with open(input_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="|")
            
            for row in reader:
                if len(row) != 3:
                    continue
                user_id, relation_type, target_id = row
                if relation_type not in RELATION_MAP:
                    continue

                field = RELATION_MAP[relation_type]

                # Insert new user document
                doc = {"user_id": user_id, field: [target_id]}
                repo.insert_one(collection_name, doc)

                count += 1
                if count % 1000 == 0:
                    logger.info(f"Processed {count} lines.")

        logger.info(f"Completed import. Total relationships processed: {count}")
    except Exception as e:
        logger.error(f"Failed to import data from '{input_file}': {e}")
