import os

from dotenv import find_dotenv, load_dotenv
import redis.asyncio as redis

_ = load_dotenv(find_dotenv())

HOST = os.getenv("redis-host")
PORT = int(os.getenv("redis-port"))
DB = os.getenv("redis-db-ai")
USERNAME = os.getenv("redis-username")
PASSWORD = os.getenv("redis-password")

redis_client = redis.Redis(host=HOST, port=PORT, username=USERNAME, db=DB, password=PASSWORD)
