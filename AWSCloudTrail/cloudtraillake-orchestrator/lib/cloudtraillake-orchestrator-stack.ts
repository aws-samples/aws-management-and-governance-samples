import { Duration, Stack, StackProps, CfnResource, CfnParameter } from 'aws-cdk-lib';
import { Config } from '../config';
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as iam from "aws-cdk-lib/aws-iam";
import * as kms from 'aws-cdk-lib/aws-kms';
import * as sns from "aws-cdk-lib/aws-sns";
import * as subscriptions from "aws-cdk-lib/aws-sns-subscriptions";
import { Construct } from 'constructs';
import { StateMachine } from '@matthewbonig/state-machine'
import * as fs from "fs";

export class CloudtraillakeOrchestratorStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Get the eventDataStore and email address from the config or from paramaters
    var eventDataStoreArn;
    if ( Config.CloudtraillakeEventDataStoreArn ) {
      eventDataStoreArn = Config.CloudtraillakeEventDataStoreArn
    }
    else {
      //console.log("CloudtraillakeEventDataStoreArn not defined in config.ts. Must be passed in as a parameter.")
      eventDataStoreArn = new CfnParameter(this, "CloudtraillakeEventDataStoreArn", {
        type: "String",
        allowedPattern: '^arn:aws:cloudtrail:.*',
        description: "The ARN of the CloudTrail Lake Event Data Store. Permission will be given to the Lambda function to query this event data store."
        }).valueAsString;
    }

    var emailAddress;
    if ( Config.NotifyEmailAddress ) {
      emailAddress = Config.NotifyEmailAddress;
    }
    else {
      emailAddress = new CfnParameter(this, "NotifyEmailAddress", {
        type: "String",
        allowedPattern: '.+\@.+',
        description: "The email address which will recieve notifications from SNS for any service limit quota limits that are requested. Note: you will need to check your inbox after deploying the CDK and confirm the SNS subscription"
        }).valueAsString;
    }
    
    // The Lambda function for querying the CloudTrail Lake, in Python
    const lambda_inline = fs.readFileSync('lambda/cloudtraillake-query.py','utf8');
    const handler = new lambda.Function(this, "CloudtraillakeQueryHandler", {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromInline(lambda_inline),
      handler: "index.lambda_handler",
      timeout: Duration.minutes(5),
      environment: {
        EVENT_DATA_STORE: eventDataStoreArn
      }
    });
    // give it an ID that is easier to find
    (handler.node.defaultChild! as CfnResource).overrideLogicalId('CloudtraillakeQuery');

    // Add an IAM policy to the Lambda role to give it permission to query CloudTrail Lake event data store
    const statement = new iam.PolicyStatement();
    statement.addActions("cloudtrail:startQuery");
    statement.addActions("cloudtrail:getQueryResults");
    statement.addResources(eventDataStoreArn);
    handler.addToRolePolicy(statement); 
    
    // Create a KMS key for encrypting the SNS topic
    const key = new kms.Key(this, "ServiceLimitCheckerKey");
    
    // Add an SNS topic for the Step Functions state machine to notify
    const topic = new sns.Topic(this, 'ServiceLimitChecker', {
      masterKey: key
    });
    topic.addSubscription(new subscriptions.EmailSubscription(emailAddress));

    // Create a role to for Step Functions state machine 
    const sfRole = new iam.Role(this, 'Role', {
        assumedBy: new iam.ServicePrincipal('states.amazonaws.com'),
        description: 'Role for CloudtraillakeOrchectrator state machine to interface with other AWS resources',
    });
    // permission to invoke cloudtrail lake query function
    handler.grantInvoke(sfRole);
    // permission to publish to the SNS topic
    topic.grantPublish(sfRole);
    // permission to encrypt via KMS to the SNS topic
    key.grantEncryptDecrypt(sfRole)

    // step functions state machine
    new StateMachine(this, 'CloudtraillakeOrchestrator', {
      role: sfRole,
      definition: JSON.parse(fs.readFileSync('step-functions/state-machine.json').toString()),
      // this is where to provide dynamic/variable overrides to the state machine definition
      overrides: {
        "CloudtraillakeQuery_RequestServiceQuotaIncrease": {
          "Parameters": {
            "FunctionName": handler.functionArn,
            "Payload": {
              "EventDataStore": "FROM_ENV"
            }
          }
        },
        "Each_RequestServiceQuotaIncrease": {
          "Iterator": {
            "States" : {
              "CloudtraillakeQuery_UpdateServiceQuotaIncreaseRequestStatus": {
                "Parameters": {
                  "FunctionName": handler.functionArn,
                  "Payload": {
                    "EventDataStore": "FROM_ENV"
                  }
                }
              },
              "Send_Report": {
                "Parameters": {
                  "TopicArn": topic.topicArn
                }
              }
            }
          }
        }
      }
    });
  }
}
