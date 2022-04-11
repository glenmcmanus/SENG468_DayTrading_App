require('dotenv').config()
const redis = require('redis');
const client = redis.createClient({ url: process.env.REDIS_URL });
const getId = require('docker-container-id');
var consumer_name = null;
const group = 'web_api';
const streams = ['command_out', 'quote_out'];

var response_buffer = {}

async function connect() {

    console.log(process.argv[2]);

    await client.connect();

    consumer_name = await getId();
    console.log("Container name:" + consumer_name);

    for(let i = 0; i < streams.length; i++)
        await createConsumerGroup(streams[i], group);

    //await createConsumerGroup(streams[0], group);
    //await createConsumerGroup(stream[1], group);

    //let payload = {'msg': `hello from web api ${consumer_name}`};
    //payload = JSON.stringify(payload);
    //await writeStream('command_in', payload);
    //await writeStream('quote_in', payload);
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

async function writeStream(stream, payload, res) {
    const id = await client.xAdd(stream, '*', payload);
    response_buffer[id] = res;

    console.log("wrote stream with id: " + id);
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
exports.response_buffer = response_buffer;
exports.consumer_name = consumer_name;