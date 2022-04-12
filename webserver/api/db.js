require('dotenv').config()
const mongoose = require("mongoose");
const dns = require('dns')
const redisClient = require('./redis_client.js')


const options = {
  family: 4,
};

const url = process.env.DATABASEURL;

const connectionParams = {
  useNewUrlParser: true,
  useUnifiedTopology: true,
};

const logObject = { name: "Company Inc", address: "Highway 37" };

const userSchema = new mongoose.Schema({UserID: String,
                              FirstName: String,
                              LastName: String,
                              AccountBalance: Number,
                              Email: String,
                              Password: String,
                              PhoneNumber: String,
                              AccessToken: String,
                              PendingBuy: {},
                              PendingSell: {}});
var User = null;
var EventLog = null;

function connectDB () {

    console.log("Attempt connection to " + url);

    mongoose
    .connect(url, connectionParams)
    .then(() => {
      console.log("Connected to database ");
      User = mongoose.model('User', userSchema, 'User');
      EventLog = mongoose.model('EventLog', {}, 'EventLog');
    })
    .catch((err) => {
      console.error(`Error connecting to the database. \n${err}`);
      console.log("Retry connection in 10s...");
      setTimeout(connectDB, 10000);
    });
}

async function register(userid) {
    if(User == null)
        return "DB not connected!";

    if(redisClient.hashExists('user', userid) == true)
        return "User exists";

    const existence = await User.find({UserID:userid});
    if(existence.length > 0)
    {
        redisClient.setHash('user', userid, existence);
        return "User exists";
    }

    const user = new User({UserID: userid, AccountBalance:0.00});
    redisClient.setHash(userid, 'balance', 0.00);

    console.log("Pre-save " + userid + ":\n\n" + JSON.stringify(user));

    user.save(function (err) {
      if (err)
        console.log(err);
    });

    //User.create({UserID: userid}, (error, doc) => {
    //    console.log(error);
    //});

    return "User registered";
}

async function dropAll() {
    if(User != null)
        await User.deleteMany({});

    if(EventLog != null)
        await EventLog.deleteMany({});
}

async function dumpLog(userid='') {
    if(userid != '')
        return await EventLog.find({UserID:userid});
    else
        return await EventLog.find({});
}

async function findUser(userid) {
    return await User.find({UserID:userid});
}

exports.dropAll = dropAll;
exports.connectDB = connectDB;
exports.register = register;
exports.dumpLog = dumpLog;
exports.findUser = findUser;