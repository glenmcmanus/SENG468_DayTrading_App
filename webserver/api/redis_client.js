require('dotenv').config()
const redis = require('redis');
const client = redis.createClient({ url: process.env.REDIS_URL });
const getId = require('docker-container-id');

var consumer_id = null;
const group = 'web_api';
const streams = ['command_out', 'quote_out'];

async function connect() {
    await client.connect();
    consumer_id = await getId();

    for(let i = 0; i < streams.length; i++)
        await createConsumerGroup(streams[i], group);
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

async function writeStream(stream, payload) {
    return await client.xAdd(stream, '*', payload);
}

async function createConsumerGroup(stream, group) {
    try {
        await client.xGroupCreate(stream, group, '0', {
            MKSTREAM: true
        });
    } catch (e) {
        console.log('Consumer group already exists, skipped creation.');
    }
}

async function listenForId(stream, id) {
    for(;;)
    {
        try {
            let response = await client.xReadGroup(
                client.commandOptions({
                    isolated: true
                }),
                'web_api',
                consumer_id, [
                    // XREADGROUP can read from multiple streams, starting at a
                    // different ID for each...
                {
                    key: stream,
                    id: '>'
                }
                ], {
                    // Read 1 entry at a time, block for 5 seconds if there are none.
                    COUNT: 1,
                    BLOCK: 5000
                }
            );

            if (response) {
                no_response = false;

                console.log(response);

                if(response[0].messages[0].id == id);
                {
                    client.xAck(stream, group, id);
                    return response;
                }

            } else {
                    // Response is null, we have read everything that is
                    // in the stream right now...
                    //console.log('No new stream entries.');
            }
        } catch (err) {
            console.error(err);
        }
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
exports.consumer_id = consumer_id;
exports.listenForId = listenForId;
