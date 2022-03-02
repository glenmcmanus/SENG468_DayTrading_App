var express = require('express');
var router = express.Router();
var transaction_client = require('../transaction_client.js');

/* GET users listing. */
router.get('/', function(req, res, next) {
//res.render('index', { title: 'CANCEL' });
  res.send('CANCEL');
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', (req, res) => {
    console.log(req.body);

    const query = CONST.CANCEL_SELL + ',' + req.body['userID'];
    transaction_client.enqueue(req.body['userID'], query, res);
});

module.exports = router;
