var express = require('express');
var router = express.Router();

const CONST = require("../public/javascripts/constants");
const redis = require('../redis_client');
const mongo = require('../db')


/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('DISPLAY_SUMMARY');
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
});
  
router.put('/', async (req, res) => {
    console.log(req.body);

    user = await db.findUser(req.body['userID']);
    if(user.length > 0)
        res.send(user);
    else
        res.send("User not found.");
    }

});

module.exports = router;
