var net = require('net');

const fetch_ip = process.env.FETCH_IP;
const fetch_port = process.env.FETCH_PORT;

var fetch_buffer = {}
var fetch_client = new net.Socket();

function connect() {
    fetch_client.connect(fetch_port, fetch_ip, function() {
        console.log('Connected to fetch service');
    });
}

fetch_client.on('data', function(data) {
	console.log('Received: ' + data);
});

function enqueue(userid, query, res) {
    fetch_buffer[userid] = res;
    fetch_client.write(req.body["userID"] + ',' + req.body["stock"]);
}

exports.connect = connect;
exports.enqueue = enqueue;