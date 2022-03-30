var net = require('net');

var fetch_buffer = {}
var fetch_client = new net.Socket();

function connect() {
    fetch_client.connect(process.env.FETCH_PORT, 'fetch_server', function() {
        console.log('Connected to fetch service');
    });
}

fetch_client.on('data', function(data) {
	console.log('Received: ' + data);
    const result = data.toString().split(',');
    fetch_buffer[result[0]].send(data);
});

function enqueue(userid, query, res) {
    fetch_buffer[userid] = res;
    fetch_client.write(req.body["userID"] + ',' + req.body["stock"]);
}

exports.connect = connect;
exports.enqueue = enqueue;