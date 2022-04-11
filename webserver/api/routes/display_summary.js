const CONST = require("../public/javascripts/constants");
const redis = require('../redis_client');
const mongo = require('../db')

var express = require('express');
var router = express.Router();

const redis_client = require('../redis_client.js');
const redis_listener = require('../redis_listener')

/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('DISPLAY_SUMMARY');
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', (req, res) => {
    console.log(req.body);

    if(redis.hashExists('user', req.body['userID']))
    {
        res.send(redis.getHash('user', req.body['userID']));
    }
    else
    {
        user = db.findUser(req.body['userID']);
        if(user.length > 0)
            res.send("Summary for " + req.body['userID']);
        else
            res.send("Summary for " + req.body['userID']);
    }

});

module.exports = router;
