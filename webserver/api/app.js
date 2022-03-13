var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors = require("cors");
var mgdb = require('./db.js');

var indexRouter = require('./routes/index');
var addRouter = require('./routes/add');
var buyRouter = require('./routes/buy');
var sellRouter = require('./routes/sell');
var cancelRouter = require('./routes/cancel');
var commitRouter = require('./routes/commit');
var dumplogRouter = require('./routes/dumplog');
var quoteRouter = require('./routes/quote');
var set_buyRouter = require('./routes/set_buy');
var set_sellRouter = require('./routes/set_sell');
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
app.use('/cancel', cancelRouter);
app.use('/commit', commitRouter);
app.use('/dumplog', dumplogRouter);
app.use('/quote', quoteRouter);
app.use('/set_buy', set_buyRouter);
app.use('/set_sell', set_sellRouter);

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

mgdb.connectDB();

module.exports = app;
