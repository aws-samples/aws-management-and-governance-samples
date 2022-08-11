import { Duration, Stack, StackProps, CfnResource, CfnParameter } from 'aws-cdk-lib';
import { Config } from '../config';
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as iam from "aws-cdk-lib/aws-iam";
import * as sns from "aws-cdk-lib/aws-sns";
import * as subscriptions from "aws-cdk-lib/aws-sns-subscriptions";
import { Construct } from 'constructs';
import { StateMachine } from '@matthewbonig/state-machine'
import * as fs from "fs";

export class CloudtraillakeOrchestratorStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Required config (in ../config.ts)
    const eventDataStoreArn = Config.CloudtraillakeEventDataStoreArn;
    const eventDataStoreId = eventDataStoreArn.split('/')[1];
    const emailAddress = Config.NotifyEmailAddress;
    
    // The Lambda function for querying the CloudTrail Lake, in Python
    const handler = new lambda.Function(this, "CloudtraillakeQueryHandler", {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset("lambda"),
      handler: "cloudtraillake-query.lambda_handler",
      timeout: Duration.minutes(5),
      environment: {
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
    
    // Add an SNS topic for the Step Functions state machine to notify
    const topic = new sns.Topic(this, 'ServiceLimitChecker');
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

    // step functions state machine
    new StateMachine(this, 'CloudtraillakeOrchestrator', {
      stateMachineName: 'CloudtraillakeOrchestrator',
      role: sfRole,
      definition: JSON.parse(fs.readFileSync('step-functions/state-machine.json').toString()),
      // this is where to provide dynamic/variable overrides to the state machine definition
      overrides: {
        "CloudtraillakeQuery_RequestServiceQuotaIncrease": {
          "Parameters": {
            "FunctionName": handler.functionArn,
            "Payload": {
              "EventDataStore": eventDataStoreId,
              "QueryFormatParams": {
                "EventDataStore": eventDataStoreId,
              }
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
                    "EventDataStore": eventDataStoreId,
                    "QueryFormatParams": {
                      "EventDataStore": eventDataStoreId
                    }
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
