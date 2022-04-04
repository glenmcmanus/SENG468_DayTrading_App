require('dotenv').config()
const redis = require('redis');
const listener = require('./redis_listener');

const client = redis.createClient({ url: process.env.REDIS_URL });

async function connect() {
    await client.connect();
}

async function setHash(collection, key, json_value) {
    client.hset(collection, key, json_value, function (err, response) {
        if (err) {
            logger.log({"level": "error", "message": JSON.stringify(err)});
        }
    });
}

async function getHash(collection, key) {
    return await client.hget(collection, key);
}

async function hashExists(collection, key) {
    return await client.hexists(collection, key);
}

function delHash(collection, key) {
    return client.hdel(collection, key, function(err) {
        if(err) {
            console.log(err)
        }
   });
}

async function writeStream(stream, payload) {
    await client.xAdd(stream, '*', {
      payload
    });
}

async function createConsumerGroup(stream) {

}

async function shutdown() {
    await client.quit();
}

exports.connect = connect;
exports.getHash = getHash;
exports.setHash = setHash;
exports.hashExists = hashExists;