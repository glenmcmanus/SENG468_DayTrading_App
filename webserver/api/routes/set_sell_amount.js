var express = require('express');
var router = express.Router();

const CONST = require("../public/javascripts/constants");
const redis_client = require('../redis_client.js');


/* GET users listing. */
router.get('/', function(req, res, next) {
 
  res.send('SET_SELL');
   
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', async (req, res) => {
    console.log(req.body);

    const id = await redis_client.writeStream('command_in', req.body);
    const response = await redis_client.listenForId('command_out', id);

    res.send(response);
});

module.exports = router;
