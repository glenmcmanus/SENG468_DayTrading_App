const redis = require('./redis_client')

const {
  Worker, isMainThread, parentPort, workerData
} = require('worker_threads');

if (isMainThread) {
    var stream_listener = new Promise((resolve, reject) => {
            const worker = new Worker(__filename, {
            workerData: redis.streams
        });

        worker.on('message', (resolve) => {
            console.log("Main thread resolved:");
            console.log(resolve);
        });

        worker.on('error', reject);

        worker.on('exit', (code) => {
            if (code !== 0) {
              reject(new Error(`Worker stopped with exit code ${code}`));
            }
        });

    });

exports.stream_listener = stream_listener;

} else {
    const streams = workerData;

    async function listen()
    {
        no_response = true;
        for(;;) {
            for(let i = 0; i < streams.length;) {
                try {
                    let response = await redis.client.xReadGroup(
                        app.redisClient.commandOptions({
                            isolated: true
                       }),
                        redis.group,
                        consumerName, [
                          // XREADGROUP can read from multiple streams, starting at a
                          // different ID for each...
                        {
                            key: streams[i],
                            id: '>'
                        }
                        ], {
                            // Read 1 entry at a time, block for 5 seconds if there are none.
                            COUNT: 1,
                            //BLOCK: 5000
                        }
                    );

                    if (response) {
                        no_response = false;
                        let response = JSON.stringify(response);
                        console.log(response);
                        parentPort.postMessage(response);

                        //todo wait until response is handled before acking
                        const entryId = response[0].messages[0].id;
                        await redis.client.xAck(streams[i], redis.group, entryId);
                    } else {
                        // Response is null, we have read everything that is
                        // in the stream right now...
                        console.log('No new stream entries.');
                        res.send("No orders exist in the stream.")
                    }
                } catch (err) {
                    console.error(err);
                    res.send("Failed to read order stream.");
                }
            }

            i = (i + 1) % streams.length;
            if(i == 0) {
                if(no_response == true)
                    await sleep(5);
                else
                    no_response = true;
            }
        }
    }

}