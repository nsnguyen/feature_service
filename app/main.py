from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import redis
import xxhash
import logging
import uuid

LOGGER = logging.getLogger(__name__)

    
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    

app = FastAPI()

r = redis.Redis(host='redis', port=6379, db=0)


@app.get("/")
def read_root():
    return {"Hello": "TESTTEST "}


@app.post("/feature")
async def create_feature(user: User):
    LOGGER.info('=====create_feature=====')
    first_name = xxhash.xxh32('first_name', seed=0).hexdigest()
    r.hset(user.id , first_name, user.first_name)
    
    last_name = xxhash.xxh32('last_name', seed=0).hexdigest()
    r.hset(user.id, last_name, user.last_name)
    return user


@app.get("/feature/{id}/{feature_name}")
async def get_feature(id:int, feature_name: str):
    LOGGER.info('=====get_feature=====')
    feature = xxhash.xxh32(feature_name, seed=0).hexdigest()
    r.hget(id, feature)
    return r.hget(id, feature)