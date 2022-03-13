const mongoose = require("mongoose");
require('dotenv').config()

const url = process.env.DATABASEURL;

const connectionParams = {
  useNewUrlParser: true,
  useUnifiedTopology: true,
};

const logObject = { name: "Company Inc", address: "Highway 37" };

function connectDB () {

    console.log("Attempt connection to " + url);

    mongoose
    .connect(url, connectionParams)
    .then(() => {
      console.log("Connected to database ");
    })
    .catch((err) => {
      console.error(`Error connecting to the database. \n${err}`);
      console.log("Retry connection in 10s...");
      setTimeout(connectDB, 10000);
    });
}

exports.connectDB = connectDB;
