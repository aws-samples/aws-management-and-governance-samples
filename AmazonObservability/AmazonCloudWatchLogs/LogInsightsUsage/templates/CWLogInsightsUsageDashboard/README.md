# CloudWatch Custom Widget for Log Insights Query History

## Overview

This CloudFormation template deploys an AWS Lambda function and an optional CloudWatch Dashboard to display a custom widget. The widget lists all the queries executed in CloudWatch Logs Insights in the last few days, ordered by the amount of bytes scanned. This is useful for identifying queries that scan a lot of data and may be candidates for optimization.

## Parameters

- **DoCreateExampleDashboard**: 
  - **Description**: Create the Dashboard to show the widget. Select `No` to deploy the Lambda function only.
  - **Type**: String
  - **Allowed Values**: `['Yes', 'No']`
  - **Default**: `Yes`

## Conditions

- **CreateExampleDashboard**: This condition checks if `DoCreateExampleDashboard` is set to `Yes`.

## Resources

### Lambda Function

- **Type**: `AWS::Lambda::Function`
- **Properties**:
  - **Code**: Inline Python code that:
    - Obtains the current AWS region.
    - Uses the `boto3` library to interact with CloudWatch Logs.
    - Fetches and sorts query history by bytes scanned.
    - Generates an HTML table of the query history.
  - **Description**: "CloudWatch Custom Widget for Log Insights query history"
  - **FunctionName**: `${AWS::StackName}`
  - **Handler**: `index.lambda_handler`
  - **MemorySize**: `128`
  - **Role**: IAM Role with permissions to access CloudWatch Logs
  - **Runtime**: `python3.11`
  - **Timeout**: `60` seconds
  - **Tags**:
    - `Key`: `cw-custom-widget`
    - `Value`: `describe:readOnly`

### IAM Role for Lambda

- **Type**: `AWS::IAM::Role`
- **Properties**:
  - **AssumeRolePolicyDocument**: Allows Lambda to assume this role.
  - **Policies**:
    - Permissions to create log groups, streams, and put log events.
    - Permissions to describe and get query results from CloudWatch Logs.

### Log Group for Lambda

- **Type**: `AWS::Logs::LogGroup`
- **Properties**:
  - **LogGroupName**: `/aws/lambda/${AWS::StackName}`
  - **RetentionInDays**: `7`

### CloudWatch Dashboard (Optional)

- **Type**: `AWS::CloudWatch::Dashboard`
- **Condition**: `CreateExampleDashboard`
- **Properties**:
  - **DashboardName**: `${AWS::StackName}-${AWS::Region}`
  - **DashboardBody**: JSON that includes a custom widget pointing to the Lambda function's ARN.

## Usage

1. **Deploy the Stack**:
   - Use the AWS Management Console, AWS CLI, or any other AWS SDK to deploy this CloudFormation template.
   
2. **View the Dashboard** (if created):
   - Navigate to the CloudWatch service in the AWS Management Console.
   - Open the dashboard named `${AWS::StackName}-${AWS::Region}` to view the custom widget.

## Notes

- The Lambda function has a timeout of 60 seconds. Adjust this if your query history is extensive.
- The log group retention is set to 7 days. Modify this as needed.

