var net = require('net');

var transaction_buffer = {}
var transaction_client = new net.Socket();

function connect() {
    transaction_client.connect(process.env.TRANSACTION_PORT, 'transaction_server', function() {
        console.log('Connected to transaction service')
    });
}

transaction_client.on('data', function(data) {
    console.log('From transaction, received ' + typeof(data) +': ' + data);
    const result = data.toString().split(',');
    transaction_buffer[result[0]].send(data);
});

function enqueue(userid, query, res) {
    console.log("enqueue");

    console.log("Send query: " + query);
    transaction_buffer[userid] = res;
    transaction_client.write(query);
}

exports.connect = connect;
exports.enqueue = enqueue;