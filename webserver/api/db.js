const mongoose = require("mongoose");

const url = `mongodb+srv://jschriemer:sengproject@cluster0.gr3il.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`;

const connectionParams = {
  useNewUrlParser: true,
  useUnifiedTopology: true,
};

const logObject = { name: "Company Inc", address: "Highway 37" };

exports.connectDB = function () {
  mongoose
    .connect(url, connectionParams)
    .then(() => {
      console.log("Connected to database ");
    })
    .catch((err) => {
      console.error(`Error connecting to the database. \n${err}`);
    });
};
