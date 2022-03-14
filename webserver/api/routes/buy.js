const CONST = require("../public/javascripts/constants");

var express = require('express');
var router = express.Router();
var transaction_client = require('../transaction_client.js');

/* GET users listing. */
router.get('/', function(req, res, next) {
//res.render('index', { title: 'BUY' });
  res.send('BUY');
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', (req, res) => {
    console.log("put: " + JSON.stringify(req.body));

    const query = CONST.BUY + ',' + req.body['userID'] + ',' + req.body['stock'] + ',' + req.body['value'];

    console.log("query: " + query);

    transaction_client.enqueue(req.body['userID'], query, res);
});

module.exports = router;
