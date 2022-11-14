# Welcome to the CloudTrail Lake Orchestrator project

This CDK project deploys a Lambda function which can be used to make querying CloudTrail Lake easier. 
It also deploys a sample Step Functions state machine which demonstrates how you can easily orchestrate
your business logic.

## Sample state machine - AWS Service Limits

The sample state machine will query AWS service limits for pending and resolved quota increases. This is a easy and quick way for customers to know which service limits were increased over a period of time across different regions and accounts. Currently customers have to login into each account and switch into each region and write down service quota history details on a piece of paper. Through the use of this solution along with CloudTrail Lake, the process can be automated.

## 3rd party npm package disclaimer

This solution requires installing a 3rd party package that is not owned or maintained by AWS. The package is a CDK construct called "@matthewbonig/state-machine". You can ready about it [here](https://www.npmjs.com/package/@matthewbonig/state-machine) and in this [blog](https://matthewbonig.com/2022/02/19/step-functions-and-the-cdk/). Matthew was featured on episode 031 of the [AWS Developer Podcast](https://aws.amazon.com/developer/podcast/). 

## Getting started

1. Create a CloudTrail Lake event data store from the [CloudTrail Lake console](https://console.aws.amazon.com/cloudtrailv2/home#/lake). Copy the event data store ARN from the Event data stores tab in the console. 
2. [Optional] Create an AWS Cloud9 environment from the [AWS Cloud9 console](https://console.aws.amazon.com/cloud9/home) if you do not already have an environment for deploying CDK projects. 
3. Check out this GitHub repository in your environment using `git clone`
4. Update the *CloudtraillakeEventDataStoreArn* variable in the [config.ts](config.ts) file with the ARN of the event data store you copied in step 1. Save the file.
5. Run `npm i @matthewbonig/state-machine` to install the 3rd party npm package.
6. Run `npm run build` to compile the typecript
7. Run `cdk bootstrap aws://{account-id}/{region}` with your AWS account ID and the region to which you will deploy this solution. You may need to run `npm install -g aws-cdk` if you get an error about the CDK version being outdated in your environment.
8. Run `cdk synth` to generate the Cloudformation template.
9. Run `cdk deploy` to deploy the stack

After the solution is deployed, go to the [AWS Step Functions console](https://console.aws.amazon.com/states/home#/statemachines) to view the state machine and start an execution to see it in action. The sample state machine depends on having a service limit quota increase request pending or completed.

## When editing your state machine

You can use this project as a base to get started building your own business logic. 
1. Edit [lib/cloudtraillake-orchestrator-stack.ts](lib/cloudtraillake-orchestrator-stack.ts) with any resources you would like deployed as part of the solution. Visit this [CDK Workshop](https://cdkworkshop.com/) to learn more.
2. You can use Step Functions Workflow Studio to modify your state machine visually, and then copy the JSON definition and paste it into [step-functions/state-machine.json](step-functions/state-machine.json). 
3. Then if you need any overrides added, those are defined in the *overrides* parameter of the state machine in [lib/cloudtraillake-orchestrator-stack.ts](lib/cloudtraillake-orchestrator-stack.ts)
4. After making your desired changes, save the files, and run `cdk synth` and `cdk deploy`. Optionally, you can run `cdk watch` to hot-swap deploy whenever you save a file while you are developing.

## Cloudformation deployment

If you set both variables in config.py to an empty string it will read from CFN parameters instead. 
Grab the output from `cdk synth` to create a one-click deployment to Cloudformation. 
Running `cdk deploy CloudtraillakeEventDataStoreArn='full_arn_of_your_event_store' --parameters NotifyEmailAddress='your_email'` is functionality equivalent to `cdk deploy`.

* Note: Deploying via Cloudformation limits your ability to incorporate your Step Functions state machine changes back into the CDK project. If you intend to adapt this solution to meet your business objectives, stick with `cdk deploy`

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
