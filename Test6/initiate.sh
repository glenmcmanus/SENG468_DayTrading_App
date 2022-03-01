#!/bin/bash

docker --version

docker-compose exec cfg_srv1 sh -c "mongosh < /scripts/init-configserver.js"

docker-compose exec shard1a sh -c "mongosh < /scripts/init-shard01.js"
docker-compose exec shard2a sh -c "mongosh < /scripts/init-shard02.js"
docker-compose exec shard3a sh -c "mongosh < /scripts/init-shard03.js"

docker-compose exec router1 sh -c "mongosh < /scripts/init-router.js"

#docker-compose exec router1 mongo --port 27017
#sh.enableSharding("OnlineBookstore")
#db.adminCommand( { shardCollection: "OnlineBookstore.Orders", key: { supplierId: "hashed" } } )

#docker-compose exec router1 mongosh -c "sh.enableSharding(\"OnlineBookstore\")"
#docker-compose exec router1 mongosh -c "db.adminCommand({shardCollection: \"OnlineBookstore.Orders\", key: {supplierID: \"hashed\" } } )"