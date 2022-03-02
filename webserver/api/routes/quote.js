var express = require('express');
var router = express.Router();

var fetch_client = require('../fetch_client.js')

/* GET users listing. */
router.get('/', function(req, res, next) {
 
  res.send('QUOTE');
   
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', (req, res) => {
    console.log(req.body);

    fetch_client.client.write(req.body["userID"] + ',' + req.body["stock"]);

    res.send();
});

module.exports = router;
