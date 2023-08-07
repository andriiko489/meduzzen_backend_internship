import asyncio

import redis.asyncio as redis
import nest_asyncio
from redis.commands.search.field import NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

import uuid

from schemas import quiz_schemas

nest_asyncio.apply()


async def init_redis():
    r = await redis.from_url("redis://redis:6379")
    rs = r.ft("idx:users")

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
    r = await redis.from_url("redis://redis:6379")

    next_id = await r.incr("result_id")
    await r.set(f"result:{next_id}", result.model_dump_json())
    return await r.get(f"result:{next_id}")


asyncio.run(init_redis())
