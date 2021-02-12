var AWS = require("aws-sdk");
var sns = new AWS.SNS();

exports.handler = (event, context, callback) => {

var type = event.type;
var accountid = event.accountid;

var message = {"type":type,"accountid":accountid};

var params = {
  Message: JSON.stringify(message),
  TopicArn: process.env.SNS_ARN
};
sns.publish(params, function(err, data) {
  if (err) callback(null, err.toString()); // an error occurred
  else     callback(null, params);           // successful response
});

};
