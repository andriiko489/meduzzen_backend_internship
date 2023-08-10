import asyncio
import json

import pandas as pd

import redis.asyncio as redis
import nest_asyncio
from redis.commands.json.path import Path
from redis.commands.search.field import NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

from schemas import quiz_schemas
from utils.config import settings

nest_asyncio.apply()


async def init_redis():
    redis_db = await redis.from_url(settings.redis_url)
    rs = redis_db.ft("idx:results")

    schema = (
        NumericField("$.user_id", as_name="user_id"),
        NumericField("$.company_id", as_name="company_id"),
        NumericField("$.quiz_id", as_name="quiz_id"),
        NumericField("$.answer_id", as_name="answer_id"),
        NumericField("$.is_correct", as_name="is_correct")
    )
    try:
        await rs.create_index(
            schema,
            definition=IndexDefinition(
                prefix=["result:"], index_type=IndexType.JSON
            )
        )
    except:
        print("Index already exist, skipping init")


async def add_result(result: quiz_schemas.RedisSchema):
    redis_db = await redis.from_url(settings.redis_url)

    next_id = await redis_db.incr("result_id")
    await redis_db.json().set(f"result:{next_id}", Path.root_path(), json.loads(result.model_dump_json()))
    await redis_db.expire(f"result:{next_id}", 172800)

    return await redis_db.json().get(f"result:{next_id}")


async def get_by_user_id(user_id: int):
    await init_redis()
    redis_db = await redis.from_url(settings.redis_url)
    index = redis_db.ft("idx:results")
    res = await index.search(Query(f'@user_id: [{user_id}, {user_id}]'))
    return res


async def get_by_company_id(company_id: int):
    await init_redis()
    redis_db = await redis.from_url(settings.redis_url)
    index = redis_db.ft("idx:results")
    res = await index.search(Query(f'@company_id: [{company_id}, {company_id}]'))
    return res


async def get_by_company_id_user_id(user_id: int, company_id: int):
    await init_redis()
    redis_db = await redis.from_url(settings.redis_url)
    index = redis_db.ft("idx:results")
    res = await index.search(Query(f'@company_id: [{company_id}, {company_id}] @user_id: [{user_id}, {user_id}]'))
    return res


async def get_csv_all():
    redis_db = await redis.from_url(settings.redis_url)
    index = redis_db.ft("idx:results")
    items = (await index.search(Query("*"))).docs
    d = dict()
    for item in items:
        item = str(item)
        item = eval(item[item.index("{"):])
        js = eval(item["json"])
        for key in js.keys():
            if not d.get(key):
                d[key] = []
            d[key].append(js[key])
    return pd.DataFrame.from_dict(d)


asyncio.run(init_redis())
