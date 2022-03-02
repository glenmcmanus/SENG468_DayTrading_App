var express = require('express');
var router = express.Router();
var transaction_client = require('../transaction_client.js');

/* GET users listing. */
router.get('/', function(req, res, next) {
 
  res.send('SET_BUY');
   
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', (req, res) => {
    console.log(req.body);
    const query = CONST.SET_BUY_TRIGGER + ',' + req.body['userID'] + ',' + req.body['stock'] + ',' + req.body['amount'];
    transaction_client.enqueue(req.body['userID'], query, res);
});

module.exports = router;
