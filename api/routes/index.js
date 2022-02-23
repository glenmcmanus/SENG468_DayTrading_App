var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/', (req, res) => {
  res.send('Got a POST request')
})

router.put('/user', (req, res) => {
  res.send('Got a PUT request at /user')
})

router.delete('/user', (req, res) => {
  res.send('Got a DELETE request at /user')
})

router.get('/api/getList', (req, res) => {
  const list = ['item1', 'item2', 'item3'];
  res.json(list);
  console.log('sent list of items');
})

module.exports = router;
