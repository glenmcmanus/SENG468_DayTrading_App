var net = require('net');

const fetch_ip = process.env.FETCH_IP;
const fetch_port = process.env.FETCH_PORT;

var fetch_buffer = {}

var fetch_client = new net.Socket();
fetch_client.connect(fetch_port, fetch_ip, function() {
	console.log('Connected to fetch service');
});

fetch_client.on('data', function(data) {
	console.log('Received: ' + data);
});

exports.client = fetch_client;