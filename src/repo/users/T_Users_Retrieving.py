from neo4j import GraphDatabase
import pandas as pd
import os

if os.getenv("red_eye_state", "development") == "development":
    from dotenv import load_dotenv
    load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(user, password))

def fetch_T_users(driver=driver):
    print('Loading Users Data Started ...')

    query = """
    MATCH (u:T_User)
        RETURN u.userId AS id, 
        u.attention_ratio AS attention_ratio , 
        u.behavior_label AS behavior_label, 
        u.engagement_balance AS engagement_balance, 
        u.receiver_count AS receiver_count, 
        u.sender_count AS sender_count
    """
    with driver.session() as session:
        result = session.run(query)
        data = [record.data() for record in result]

    print('Loading Users Data Done ...')
    return pd.DataFrame(data)