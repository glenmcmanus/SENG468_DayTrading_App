var express = require('express');
var router = express.Router();
const logger = require('morgan');
const cors = require('cors');

require('dotenv').config();
const ip = process.env.WEBSERVER_IP;
const port = process.env.WEB_PORT;

router.use(
  cors({
    //if(ip == null)
    //    origin: 'http://localhost:9000',
    //else
    origin: ip + ':' + port,

    credentials: true,
  })
);

router.use(logger('dev'));
router.use(express.json());
router.use(express.urlencoded({ extended: false }));

/* GET home page. */
router.get('/', function(req, res, next) {
  console.log("query:" + req.query);
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

router.get('/api/searchTerm', function(req, res) {
  console.log('search term');
  res.writeHead(200, {
    'Content-Type': 'application/json',
  });
  console.log('Search term : ', JSON.stringify(stocks));
  res.end(JSON.stringify(stocks));
});

router.post('/api/searchTerm', function(req, res) {
  let stockSearch = req.body.stock;
  console.log('search for ' + stockSearch);
});


router.get('/api/getList', (req, res) => {
  const list = [
    { name: "MSFT", shares: 2, price: 200  },
    { name: "AMZN", shares: 1, price: 200 },
    { name: "AAPL", shares: 10, price: 400 },
  ];
  res.json(list);
  console.log('sent list of items');
})


module.exports = router;
