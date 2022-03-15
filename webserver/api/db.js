const mongoose = require("mongoose");
require('dotenv').config()

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
    const existence = await User.find({UserID:userid});
    if(existence.length > 0)
        return "User exists";

    const user = new User({UserID: userid, AccountBalance:0.00});

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
}

async function dumpLog(userid='') {
    if(userid != '')
        return await EventLog.find({UserID:userid});
    else
        return await EventLog.find({});
}


exports.dropAll = dropAll;
exports.connectDB = connectDB;
exports.register = register;
exports.dumpLog = dumpLog;