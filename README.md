# feature_service

## To ssh into redis
```
docker exec -it redis redis-cli
```

## curl POST
```
curl -d '{
    "id": 1,
    "first_name": "Santa",
    "last_name": "Claus",
    "large_payload": "qC76miCl05XITh2E3J8ddq3KYkzw04ky7WbTgBmJ1UzyTY9tXVsXOrl0Syld0leExmnCixCd0nfhF9yfkaB0GvPsNCLhtsrqA2Aa4tsL9"}' -H "Content-Type: application/json" -X POST http://0.0.0.0:8001/write_feature
```

## curl GET
```
curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://0.0.0.0:8001/feature/1/last_name
```