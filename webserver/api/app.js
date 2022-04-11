var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors = require("cors");
var mgdb = require('./db.js');
var transaction_client = require('./transaction_client.js');
var fetch_client = require('./fetch_client.js')
var redis = require('./redis_client.js')
var redis_listener = require('./redis_listener.js')

var indexRouter = require('./routes/index');
var addRouter = require('./routes/add');
var buyRouter = require('./routes/buy');
var sellRouter = require('./routes/sell');
var cancelBuyRouter = require('./routes/cancel_buy');
var cancelSellRouter = require('./routes/cancel_sell');
var cancelSetBuyRouter = require('./routes/cancel_set_buy');
var cancelSetSellRouter = require('./routes/cancel_set_sell');
var commitBuyRouter = require('./routes/commit_buy');
var commitSellRouter = require('./routes/commit_sell');
var displaySummary = require('./routes/display_summary');
var dumplogRouter = require('./routes/dumplog');
var quoteRouter = require('./routes/quote');
var set_buyAmountRouter = require('./routes/set_buy_amount');
var set_buyTriggerRouter = require('./routes/set_buy_trigger');
var set_sellAmountRouter = require('./routes/set_sell_amount');
var set_sellTriggerRouter = require('./routes/set_sell_trigger');
var usersRouter = require('./routes/users');

var app = express();

require('dotenv').config();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/add', addRouter);
app.use('/users', usersRouter);
app.use('/buy', buyRouter);
app.use('/sell', sellRouter);
app.use('/cancel_buy', cancelBuyRouter);
app.use('/cancel_sell', cancelSellRouter);
app.use('/cancel_set_buy', cancelSetBuyRouter);
app.use('/cancel_set_sell', cancelSetSellRouter);
app.use('/commit_buy', commitBuyRouter);
app.use('/commit_sell', commitSellRouter);
app.use('/display_summary', displaySummary);
app.use('/dumplog', dumplogRouter);
app.use('/quote', quoteRouter);
app.use('/set_buy_amount', set_buyAmountRouter);
app.use('/set_buy_trigger', set_buyTriggerRouter);
app.use('/set_sell_amount', set_sellAmountRouter);
app.use('/set_sell_trigger', set_sellTriggerRouter);

// middleware for allowing react to fetch() from server
app.use(function(req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  res.header('Access-Control-Allow-Methods', 'PUT, POST, GET, OPTIONS');
  next();
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

//service connections

service_setup();
async function service_setup()
{
    await redis.connect();
  //  redis_listener.startListener();

    mgdb.connectDB();
}

//transaction_client.connect();
//fetch_client.connect();

module.exports = app;
