const CONST = require("../public/javascripts/constants");

var express = require('express');
var router = express.Router();
var transaction_client = require('../transaction_client.js');

const redis_client = require('../redis_client.js');
const redis_listener = require('../redis_listener')

/* GET users listing. */
router.get('/', function(req, res, next) {
 
  res.send('SELL');
   
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', async (req, res) => {
    console.log(req.body);

    const id = await redis_client.writeStream('command_in', req.body, res);
    const response = await redis_listener.listenForId('command_out', id);

    res.send(response);
});

module.exports = router;
