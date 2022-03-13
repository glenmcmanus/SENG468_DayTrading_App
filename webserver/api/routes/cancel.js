var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
//res.render('index', { title: 'CANCEL' });
  res.send('CANCEL');
});

router.post('/', (req, res) => {
    res.send('Got a POST request');
  })
  
  router.put('/', (req, res) => {
    console.log(req.body);
       res.close();
      
  })

module.exports = router;
