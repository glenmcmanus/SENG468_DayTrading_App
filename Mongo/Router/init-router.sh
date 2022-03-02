mongos --port 27017 --configdb config-srv/cfg_srv1:27017,cfg_srv2:27017,cfg_srv3:27017 --bind_ip_all

if [ $PRIMARY == 1]
then
  sleep 15
  mongosh --port 27017 --file ./init-router.js
fi