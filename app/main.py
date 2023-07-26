from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import redis
import xxhash
import logging
import uuid

LOGGER = logging.getLogger(__name__)

import zstd

    
class ShipmentGroup(BaseModel):
    id: int
    feature_version: str
    avg_spot_rate: str
    ftl_rate_count: str
    

app = FastAPI()

r = redis.Redis(host='redis', port=6379, db=0)


@app.get("/")
def read_root():
    return {"Hello": "TESTTEST "}


@app.post("/write_feature")
async def create_feature(shipment: ShipmentGroup):
    LOGGER.info('=====create_feature=====', shipment.feature_version)
    avg_spot_rate = xxhash.xxh32(f"avg_spot_rate_{shipment.feature_version}", seed=0).hexdigest()
    r.hset(shipment.id , avg_spot_rate, zstd.compress(shipment.avg_spot_rate.encode()))
    
    ftl_rate_count = xxhash.xxh32(f"ftl_rate_count_{shipment.feature_version}", seed=0).hexdigest()
    r.hset(shipment.id, ftl_rate_count, zstd.compress(shipment.ftl_rate_count.encode()))
    
    # large_payload = xxhash.xxh32('large_payload', seed=0).hexdigest()
    # # compression using zstd saves 50% of the space
    # # Ex: MEMORY USAGE 1
    # r.hset(ShipmentGroup.id, large_payload, zstd.compress(ShipmentGroup.large_payload.encode()))
    
    # # raw string is taking up a lot of space
    # # r.hset(ShipmentGroup.id, last_name, ShipmentGroup.large_payload)
    
    return {"message": "Feature created in Redis"}


@app.get("/feature/{feature_name}/version/{version}/shipment_guid/{id}")
async def get_feature(id:int, feature_name: str, version: str):
    LOGGER.info('=====get_feature=====')
    feature = xxhash.xxh32(f"{feature_name}_{version}", seed=0).hexdigest()
    value = r.hget(id, feature)
    return zstd.uncompress(value)
