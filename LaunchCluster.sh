echo $'\n\nPropping up cluster...\n\n'
docker-compose up -d

sleep 2
echo $'\n\nSleeping for 2s before init config server...\n\n'

docker-compose exec cfg_srv1 sh -c "mongosh < ./init-config.js"

echo $'\n\nSleeping for 5s before init shards...\n\n'
sleep 5

docker-compose exec shard1a sh -c "mongosh < ./init-shard.js"
docker-compose exec shard2a sh -c "mongosh < ./init-shard.js"
docker-compose exec shard3a sh -c "mongosh < ./init-shard.js"

echo $'\n\nSleeping for 10s before init router...\n\n'
sleep 10

docker-compose exec router1 sh -c "mongosh < ./init-router.js"