import argparse
import csv
import logging
from data.repo.Neo4jRepo import Neo4jRepo  # adjust the import path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RELATION_MAP = {
    "event": "ATTENDED",
    "friend": "FRIEND_WITH",
    "group": "MEMBER_OF",
    "neighbor": "NEIGHBOR_WITH"
}

NODE_MAP = {
    "event": "Event",
    "friend": "User",
    "group": "Group",
    "neighbor": "User"
}

def import_lastfm_like_file(repo: Neo4jRepo, input_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            if len(row) != 3:
                continue
            user_id, relation_type, target_id = row
            if relation_type not in RELATION_MAP:
                continue

            rel_type = RELATION_MAP[relation_type]
            user_node_label = "User"
            target_node_label = NODE_MAP[relation_type]

            # Create User node
            repo.create_node("User", {"id": user_id})
            # Create target node (Event, Group, or another User)
            repo.create_node(target_node_label, {"id": target_id})

            # Create relationship
            repo.create_relationship(
                from_label="User",
                from_key={"id": user_id},
                to_label=target_node_label,
                to_key={"id": target_id},
                rel_type=rel_type
            )