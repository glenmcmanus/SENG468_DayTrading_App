mongod --port 27017 --configsvr --replSet config-srv

if [ $PRIMARY == 1]
then
  sleep 3
  mongosh --port 27017 --file ./init-config.js
fi