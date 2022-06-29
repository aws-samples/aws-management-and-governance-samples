# Welcome to the CloudTrail Lake Orchestrator project

This CDK project deploys a Lambda function which can be used to make querying CloudTrail Lake easier. 
It also deploys a sample Step Functions state machine which demonstrates how you can easily orchestrate
your business logic.

## Sample state machine - AWS Service Limits

The sample state machine will query AWS service limits for pending and resolved quota increases. This is a easy and quick way for customers to know which service limits were increased over a period of time across different regions and accounts. Currently customers have to login into each account and switch into each region and write down service quota history details on a piece of paper. Through the use of this solution along with CloudTrail Lake, the process can be automated.

## 3rd party npm package disclaimer

This solution requires installing a 3rd party package that is not owned or maintained by AWS. The package is a CDK construct called "@matthewbonig/state-machine". You can ready about it [here](https://www.npmjs.com/package/@matthewbonig/state-machine) and in this [blog](https://matthewbonig.com/2022/02/19/step-functions-and-the-cdk/). Matthew was featured on episode 031 of the [AWS Developer Podcast](https://aws.amazon.com/developer/podcast/). 

## Getting started

1. Create a CloudTrail Lake event data store. Get its Arn and update the CloudtraillakeEventDataStoreArn variable in `config.ts`
2. `cdk deploy`

## When editing your state machine

You can use this project as a base to get started building your own business logic. Edit `lib/cloudtraillake-orchestrator-stack.ts` with any resources you would like deployed as part of the solution. You can use Step Functions Workflow Studio to modify your state machine visually, and then copy the JSON definition and paste it into `step-functions/state-machine.json`. Then if you need any overrides added, those are defined in the overrides parameter of the state machine in `lib/cloudtraillake-orchestrator-stack.ts`

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
