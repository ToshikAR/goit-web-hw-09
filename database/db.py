import os
import redis

from redis_lru import RedisLRU

from mongoengine import connect
from dotenv import load_dotenv


load_dotenv()

mon_user = os.getenv("MONGODB08_USER")
mon_password = os.getenv("MONGODB08_PASSWORD")
mon_base = os.getenv("MONGODB08_DB")
mon_domain = os.getenv("MONGODB08_HOST")

# connect to AtlasDB
connect(
    db=mon_base,
    host=f"mongodb+srv://{mon_user}:{mon_password}@{mon_domain}/?retryWrites=true&w=majority&appName=Cluster0",
)


red_password = os.getenv("REDIS_M08_PASSWORD")
red_port = os.getenv("REDIS_M08_PORT")
red_host = os.getenv("REDIS_M08_HOST")

# connect to Redis
client_redis = redis.StrictRedis(host=red_host, port=red_port, password=None)
cache_redis = RedisLRU(client_redis)
