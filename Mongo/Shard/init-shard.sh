mongod --port 27017 --shardsvr --replSet $SHARD

if [ $PRIMARY == 1]
then
  sleep 6
  mongosh --port 27017 --file ./init-shard.js
fi