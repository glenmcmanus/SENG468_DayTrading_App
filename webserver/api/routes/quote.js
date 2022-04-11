const CONST = require("../public/javascripts/constants");

var express = require('express');
var router = express.Router();
var fetch_client = require('../fetch_client.js')

const redis_client = require('../redis_client.js');
const redis_listener = require('../redis_listener')

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('QUOTE');
   
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', (req, res) => {
    console.log(req.body);

    const query = req.body["userID"] + ',' + req.body["stock"];
    fetch_client.enqueue(req.body['userID'], query, res);

    redis_client.writeStream('quote', req.body, res);
});

module.exports = router;
