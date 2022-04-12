const CONST = require("../public/javascripts/constants");

var express = require('express');
var router = express.Router();
var transaction_client = require('../transaction_client.js');

const redis_client = require('../redis_client.js');

/* GET users listing. */
router.get('/', function(req, res, next) {
//res.render('index', { title: 'ADD' });
  res.send('ADD');
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', (req, res) => {
    console.log(req.body);

    //const query = CONST.ADD + ',' + req.body['userID'] + ',' + req.body['value'];
    //transaction_client.enqueue(req.body['userID'], query, res);

    //const param1 = JSON.parse(req.body);
    //const command = JSON.stringify({param1, res});

    //console.log(command);

    redis_client.writeStream('command_in', req.body);
});

module.exports = router;
