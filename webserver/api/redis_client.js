require('dotenv').config()
const redis = require('redis');
const client = redis.createClient({ url: process.env.REDIS_URL });
const getId = require('docker-container-id');
var consumerName = null;
const group = 'web_api';
const streams = ['command_out', 'quote_out'];

var response_buffer = {}

async function connect() {

    console.log(process.argv[2]);

    await client.connect();

    consumerName = await getId();
    console.log("Container name:" + consumerName);

    for(let i = 0; i < streams.length; i++)
        await createConsumerGroup(streams[i], group);

    //await createConsumerGroup(streams[0], group);
    //await createConsumerGroup(stream[1], group);

    await writeStream('command_in', JSON.stringify({'msg': 'hello from web api' + consumerName}));
    await writeStream('quote_in', JSON.stringify({'msg': 'hello from web api' + consumerName}));
}

async function setHash(collection, key, json_value) {
    client.hSet(collection, key, json_value, function (err, response) {
        if (err) {
            logger.log({"level": "error", "message": JSON.stringify(err)});
        }
    });
}

async function getHash(collection, key) {
    return await client.hGet(collection, key);
}

async function hashExists(collection, key) {
    console.log(client);

    return await client.hExists(collection, key, (err, res) => {
        if(err)
        {
            console.log(err);
            return false;
        }
        else if(!res)
            return false;
        else
            return true;
    });
}

function delHash(collection, key) {
    return client.hDel(collection, key, function(err) {
        if(err) {
            console.log(err)
        }
   });
}

async function writeStream(stream, payload) {//, res) {
    //response_buffer[payload['userID']] = res;

    console.log('write payload ' + payload + ' to stream ' + stream);

    await client.xAdd(stream, '*', payload);
}

async function createConsumerGroup(stream, group) {
    try {
        await client.xGroupCreate(stream, group, '0', {
            MKSTREAM: true
        });
        console.log('Created consumer group ' + group + ' for stream ' + stream);
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