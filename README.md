# feature_service

## To ssh into redis
```
docker exec -it redis redis-cli
```

## curl POST
```
curl -d '{
    "id": 1,
    "feature_version": "2",
    "avg_spot_rate": "2222",
    "ftl_rate_count": "5678"
    }' -H "Content-Type: application/json" -X POST http://0.0.0.0:8001/write_feature
```

## curl GET
```
curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://0.0.0.0:8001//feature/ftl_rate_count/version/2/shipment_guid/1
```