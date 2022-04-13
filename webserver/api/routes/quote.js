var express = require('express');
var router = express.Router();

const CONST = require("../public/javascripts/constants");
const redis_client = require('../redis_client.js');


/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('QUOTE');
   
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', async (req, res) => {
    console.log(req.body);

    if(redis_client.client.exists(req.body['stock']))
        res.send(redis_client.client.get(req.body['stock']))
    else
    {
        const id = await redis_client.writeStream('quote_in', req.body);
        const response = await redis_client.listenForId('quote_out', id);

        res.send(response);
    }
});

module.exports = router;
