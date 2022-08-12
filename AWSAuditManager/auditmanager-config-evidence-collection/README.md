# Enhanced Evidence Collection with AWS Config and Audit Manager

This sample demonstrates how one can leverage custom Config rules to enhance evidence collection in Audit Manager. 
Often customers require configuration evidence tied to their Config rule. In this sample, we leverage a custom Config
rule to generate a report with compliant and non-compliant evidence stored in S3. The S3 location is available as an
annotation in the Config rule. When one creates an assessment report in Audit Manager, the annotation is also returned
and one can access the evidence report in S3 at that point. 

## Pre-requisites

* AWS Config must be enabled on the region where the rule will be deployed.
* S3 bucket to write evidence reports to.

## Deployment Instructions

Deploy the CloudFormation template in your account. The template requires an existing S3 bucket (name, region and prefix 
must be provided) as well as a name for the Config rule and evidence report. 
It will create a custom Config rule and Lambda function as well as an IAM role and AWS Systems Manager
Parameter Store parameters which are used by the Lambda function.

To test this works, go the Config console in the region where the CloudFormation template was deployed 
and access the created rule. If no AMIs exist in the region, no evidence will be generated. If AMIs (public or private)
exist, one should see a compliant or non-compliant status and an annotation to the evidence report in S3. 