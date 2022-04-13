var express = require('express');
var router = express.Router();

const CONST = require("../public/javascripts/constants");
const db = require("../db.js")


/* GET users listing. */
router.get('/', function(req, res, next) {
 
  res.send('DUMPLOG');
   
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', async function(req, res) {
    console.log(req.body);
    res.send(await db.dumpLog(req.body['userID']));
});

module.exports = router;
