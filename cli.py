import logging
from scripts.import_csv_to_mongo import import_lastfm_file
from scripts.import_csv_to_graph import import_lastfm_like_file
from data.repo.MongoDbRepo import MongoDBRepo
from data.repo.Neo4jRepo import Neo4jRepo

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class Cli:
    """
    Continuous CLI interface for MongoDB and Neo4j data import.
    Type 'help' to see available commands.
    """

    @staticmethod
    def import_to_mongo(uri: str, port: str, db: str, input_file: str, collection_name: str = "users"):
            repo = MongoDBRepo(uri, port, db)
            logger.info(f"Importing '{input_file}' into MongoDB collection '{collection_name}'...")
            import_lastfm_file(repo, input_file, collection_name)
            repo.close()

    @staticmethod
    def import_to_neo4j(uri: str, user: str, password: str, input_file: str):
            repo = Neo4jRepo(uri, user, password)
            logger.info(f"Importing '{input_file}' into Neo4j...")
            import_lastfm_like_file(repo, input_file)
            repo.close()
    
    @staticmethod
    def start():
        print("=== Interactive CLI Started ===")
        print("Type 'help' for available commands, 'exit' to quit.\n")

        while True:
            try:
                command = input("> ").strip()
                if not command:
                    continue

                if command.lower() in ("exit", "quit"):
                    print("Exiting CLI...")
                    break

                elif command.lower() == "help":
                    print("""
                            Available commands:
                            import_mongo <uri> <port> <db> <input_file> [collection_name]
                            import_neo4j <uri> <user> <password> <input_file>
                            exit
                        """)
                else:
                    parts = command.split()
                    cmd = parts[0]
                    args = parts[1:]

                    if cmd == "import_mongo":
                        if len(args) < 4:
                            print("Usage: import_mongo <uri> <port> <db> <input_file> [collection_name]")
                        else:
                            uri, port, db, input_file = args[:4]
                            collection = args[4] if len(args) > 4 else "users"
                            Cli.import_to_mongo(uri, int(port), db, input_file, collection)

                    elif cmd == "import_neo4j":
                        if len(args) < 4:
                            print("Usage: import_neo4j <uri> <user> <password> <input_file>")
                        else:
                            uri, user, password, input_file = args[:4]
                            Cli.import_to_neo4j(uri, user, password, input_file)

                    else:
                        print(f"Unknown command: {cmd}. Type 'help' for help.")

            except KeyboardInterrupt:
                print("\nExiting CLI...")
                break
            except Exception as e:
                logger.error(f"Error in command loop: {e}")
