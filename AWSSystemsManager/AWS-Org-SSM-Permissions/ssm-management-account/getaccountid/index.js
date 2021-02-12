var AWS = require("aws-sdk");
var organizations = new AWS.Organizations();

exports.handler = (event, context, callback) => {

var requestid = event.id;

 var params = {
  CreateAccountRequestId: requestid
 };
 organizations.describeCreateAccountStatus(params, function(err, data) {
   if (err) {
       console.log(err, err.stack); // an error occurred
   }
   else     
   {
       var result = data.CreateAccountStatus;
       if (result.State == 'SUCCEEDED')
       {
           callback(null, {state:result.State, result:result.AccountId});
       }
       else {
           callback(null, {state:result.State,result:"PENDING"});
       }
   }
 });

};

