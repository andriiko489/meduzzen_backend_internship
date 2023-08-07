import asyncio

import redis.asyncio as redis
import nest_asyncio
from redis.commands.search.field import NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

import uuid

from schemas import quiz_schemas
from utils.config import settings

nest_asyncio.apply()


async def init_redis():
    redis_db = await redis.from_url(settings.redis_url)
    rs = redis_db.ft("idx:users")

    schema = (
        NumericField("$.user_id", as_name="user_id"),
        NumericField("$.company_id", as_name="company_id"),
        NumericField("$.quiz_id", as_name="quiz_id"),
        NumericField("$.answer_id", as_name="answer_id"),
        NumericField("$.is_correct", as_name="is_correct")
    )

    await rs.create_index(
        schema,
        definition=IndexDefinition(
            prefix=["result:"], index_type=IndexType.JSON
        )
    )


async def add_result(result: quiz_schemas.RedisSchema):
    redis_db = await redis.from_url(settings.redis_url)

    next_id = await redis_db.incr("result_id")
    await redis_db.set(f"result:{next_id}", result.model_dump_json())

    await redis_db.expire(f"result:{next_id}", 172800)
    # DAY = 48 hours = 48 * 60 minutes = 2880 minutes = 2880 * 60 seconds = 172800

    return await redis_db.get(f"result:{next_id}")


asyncio.run(init_redis())
