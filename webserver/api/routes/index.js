var express = require('express');
var router = express.Router();
const logger = require('morgan');
const cors = require('cors');

const CONST = require("../public/javascripts/constants");

require('dotenv').config();
const ip = process.env.WEBSERVER_IP;
const port = process.env.WEB_PORT;

router.use(
  cors({
    origin: ip + ':' + port,
    credentials: true,
  })
);

router.use(logger('dev'));
router.use(express.json());
router.use(express.urlencoded({ extended: false }));

/* GET home page. */
router.get('/', function(req, res, next) {
  console.log("ADD:" + CONST.ADD);
  res.render('index', { title: 'Express' });
});

//router.get('/QUOTE', function(req, res) {
//    fetch_client.write(req.params["userid"] + ',' + req.params["StockSymbol"]);
//});

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
  console.log(req);

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
