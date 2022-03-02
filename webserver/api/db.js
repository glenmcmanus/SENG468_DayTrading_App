const mongoose = require("mongoose");

const router_ip = process.env.M_ROUTER1_IP;

const url = 'mongodb://'+router_ip+':27017/DayTrading';

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
