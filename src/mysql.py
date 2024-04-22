import aiomysql
import os
from dotenv import load_dotenv

load_dotenv()

async def connect_to_mysql():
    connection = await aiomysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_DATABASE"),
        charset="utf8mb4",
        cursorclass=aiomysql.cursors.DictCursor
    )
    return connection
