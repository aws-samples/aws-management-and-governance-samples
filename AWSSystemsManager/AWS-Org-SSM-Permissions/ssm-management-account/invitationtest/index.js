exports.handler = (event, context, callback) => {
    var accountid = "";
    var type = "";
    try {
        accountid = event.detail.requestParameters.target.id;
        type = event.detail.requestParameters.target.type;
        if (type == "ACCOUNT")
        {
            callback(null,  {state:"EXISTING", result:accountid});
        }
    } catch (e) {
        callback(null, {state:"NEW", result:"NEW"});
    }
  };
  