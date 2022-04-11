require('dotenv').config()
const redisClient = require('./redis_client');

const {
  Worker, isMainThread, parentPort, workerData
} = require('worker_threads');

const redis = require('./redis_client');


if (isMainThread) {

    console.log|("Starting listener from main thread");

    function startListener() {
        const worker = new Worker(__filename);

        worker.on('message', (resolve) => {
            //redisClient.response_buffer[resolve[0].messages[0].id].send('it works!');
        });

        worker.on('error', (reject) => {
            console.log(reject);
        });

        worker.on('exit', (code) => {
            if (code !== 0) {
                reject(new Error(`Worker stopped with exit code ${code}`));
            }
        });
    }

    async function listenForId(stream, id) {
        for(;;)
        {
            try {
                let response = await redisClient.client.xReadGroup(
                    redisClient.client.commandOptions({
                        isolated: true
                    }),
                    'web_api',
                    redisClient.consumer_name, [
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
                        redisClient.client.xAck(stream, redisClient.group, id);
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

exports.startListener = startListener;
exports.listenForId = listenForId;

} else {
    console.log("In worker, about to start listening");

    const redis = require('redis');
    const client = redis.createClient({ url: process.env.REDIS_URL });

    listen();

    async function listen()
    {
        await client.connect();
        var sleep = 0;
        no_response = true;
        for(let i = 0; i < redisClient.streams.length;) {
            console.log("Listening to stream " + redisClient.streams[i]);
            try {
                let response = await client.xReadGroup(
                    redisClient.client.commandOptions({
                        isolated: true
                    }),
                    'web_api',
                    redisClient.consumer_name, [
                        // XREADGROUP can read from multiple streams, starting at a
                        // different ID for each...
                    {
                        key: redisClient.streams[i],
                        id: '>'
                    }
                    ], {
                        // Read 1 entry at a time, block for 5 seconds if there are none.
                        COUNT: 1,
                        BLOCK: sleep
                    }
                );

                if (response) {
                    no_response = false;

                    console.log(response);

                    const entryId = response[0].messages[0].id;

                    if(entryId in redisClient.response_buffer);
                    {
                        //
                        parentPort.postMessage(response);
                        client.xAck(redisClient.streams[i], redisClient.group, entryId);
                    }

                } else {
                    // Response is null, we have read everything that is
                    // in the stream right now...
                    //console.log('No new stream entries.');
                }
            } catch (err) {
                console.error(err);
                parentPort.postMessage(err);
            }

            i = (i + 1) % redisClient.streams.length;
            if(i == redisClient.streams.length - 1) {
                if(no_response == true)
                    sleep = 5;
                else {
                    no_response = true;
                    sleep = 0;
                }
            }
        }
    }

}