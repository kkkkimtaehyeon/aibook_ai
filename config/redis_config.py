import os

from dotenv import find_dotenv, load_dotenv
import redis.asyncio as redis

_ = load_dotenv(find_dotenv())

HOST = os.getenv("REDIS_HOST")
PORT = os.getenv("REDIS_PORT")
DB = os.getenv("REDIS_DB")
USERNAME = os.getenv("REDIS_USERNAME")
PASSWORD = os.getenv("REDIS_PASSWORD")

redis_client = redis.Redis(host=HOST, port=PORT, username=USERNAME, db=DB, password=PASSWORD)
