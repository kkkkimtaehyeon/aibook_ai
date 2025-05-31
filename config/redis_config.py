import os

from dotenv import find_dotenv, load_dotenv
import redis.asyncio as redis

_ = load_dotenv(find_dotenv())

HOST = os.getenv("redis_host")
PORT = os.getenv("redis_port")
DB = os.getenv("redis_db_ai")
USERNAME = os.getenv("redis_username")
PASSWORD = os.getenv("redis_password")

redis_client = redis.Redis(host=HOST, port=PORT, username=USERNAME, db=DB, password=PASSWORD)
