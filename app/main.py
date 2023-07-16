from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import redis
import xxhash
import logging
import uuid

LOGGER = logging.getLogger(__name__)

import zstd

    
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    large_payload: str
    

app = FastAPI()

r = redis.Redis(host='redis', port=6379, db=0)


@app.get("/")
def read_root():
    return {"Hello": "TESTTEST "}


@app.post("/feature")
async def create_feature(user: User):
    LOGGER.info('=====create_feature=====')
    first_name = xxhash.xxh32('first_name', seed=0).hexdigest()
    r.hset(user.id , first_name, zstd.compress(user.first_name.encode()))
    
    last_name = xxhash.xxh32('last_name', seed=0).hexdigest()
    r.hset(user.id, last_name, zstd.compress(user.last_name.encode()))
    
    large_payload = xxhash.xxh32('large_payload', seed=0).hexdigest()
    # compression using zstd saves 50% of the space
    # Ex: MEMORY USAGE 1
    r.hset(user.id, large_payload, zstd.compress(user.large_payload.encode()))
    
    # raw string is taking up a lot of space
    # r.hset(user.id, last_name, user.large_payload)
    
    return {"message": "Feature created in Redis"}


@app.get("/feature/{id}/{feature_name}")
async def get_feature(id:int, feature_name: str):
    LOGGER.info('=====get_feature=====')
    feature = xxhash.xxh32(feature_name, seed=0).hexdigest()
    value = r.hget(id, feature)
    return zstd.uncompress(value)
