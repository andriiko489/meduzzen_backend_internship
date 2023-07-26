import redis.asyncio as redis
import nest_asyncio

nest_asyncio.apply()


async def connect_redis():
    return await redis.from_url("redis://redis:6379")


r = connect_redis()
