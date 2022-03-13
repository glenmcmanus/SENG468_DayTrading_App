var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
 
  res.send('DUMPLOG');
   
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', (req, res) => {
    console.log(req.body);
    res.send();
});

module.exports = router;
