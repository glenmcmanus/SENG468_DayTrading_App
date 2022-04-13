const CONST = require("../public/javascripts/constants");

var express = require('express');
var router = express.Router();
var fetch_client = require('../fetch_client.js')

const redis_client = require('../redis_client.js');

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('QUOTE');
   
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', (req, res) => {
    console.log(req.body);

    const id = await redis_client.writeStream('quote_in', req.body);
    const response = await redis_client.listenForId('quote_out', id);

    res.send(response);
});

module.exports = router;
