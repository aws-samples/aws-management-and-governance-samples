export const Config = {
    // The ARN of the CloudTrail Lake Event Data Store
    // Permission will be given to the Lambda function to query this event data store
    // must start with arn:aws:cloudtrail:
    CloudtraillakeEventDataStoreArn: "",
    // The email address which will recieve notifications from SNS for any service limit quota limits that are requested
    // Note: you will need to check your inbox after deploying the CDK and confirm the SNS subscription
    NotifyEmailAddress: ""
};