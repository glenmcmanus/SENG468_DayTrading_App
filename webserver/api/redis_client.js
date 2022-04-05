require('dotenv').config()
const redis = require('redis');
const client = redis.createClient({ url: process.env.REDIS_URL });
const getId = require('docker-container-id');
var consumerName = null;
const group = 'web_api';
const streams = ['out'];

async function connect() {

    console.log(process.argv[2]);

    await client.connect();

    streams.forEach(stream => {
            createConsumerGroup(stream, group);
    });

    consumerName = await getId();
    console.log("Container name:" + consumerName);

    await writeStream(streams[0], 'hello world');

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

async function createConsumerGroup(stream, group) {
    try {
        await client.xGroupCreate(stream, group, '0', {
            MKSTREAM: true
        });
        console.log('Created consumer group.');
    } catch (e) {
        console.log('Consumer group already exists, skipped creation.');
    }
}

async function shutdown() {
    await client.quit();
}

exports.client = client;
exports.connect = connect;
exports.getHash = getHash;
exports.setHash = setHash;
exports.hashExists = hashExists;
exports.streams = streams;
exports.writeStream = writeStream;
exports.consumerName = consumerName;