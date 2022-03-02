var net = require('net');

const transaction_ip = process.env.TRANSACTION_IP;
const transaction_port = process.env.TRANSACTION_PORT;

var transaction_buffer = {}
var transaction_client = new net.Socket();

function connect() {
    transaction_client.connect(transaction_port, transaction_ip, function() {
        console.log('Connected to transaction service')
    });
}

transaction_client.on('data', function(data) {
    console.log('From transaction, received ' + typeof(data) +': ' + data);
    const result = data.toString().split(',');
    transaction_buffer[result[0]].send(data);
});

function enqueue(userid, query, res) {
    transaction_buffer[userid] = res;
    transaction_client.write(query);
}

exports.connect = connect;
exports.enqueue = enqueue;