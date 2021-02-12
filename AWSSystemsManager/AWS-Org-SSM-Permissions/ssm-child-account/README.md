# ssm-child-account

This project directory includes the following files and folders:

- * **template.yaml** - CloudFormation template to deploy resources into the child account containing your SSM Documents

## Deployment Instructions

**Required parameters**:

* **SNSTopicArn**: The SNS Topic ARN resource deployed into the AWS Organizations Management account.  This SNS Topic ARN is found in the Output section in the CloudFormation stack that was created in your AWS Organizations Management account.
* **SNSTopicRegion**: The region the SNS Topic was deployed to

**Deployment**
To deploy this template via CloudFormation StackSets, please refer to the CloudFormation StackSet documentation available at this url: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-getting-started-create.html#stacksets-getting-started-create-self-managed

**Note** *This step assumes you already have created self-managed execution roles.  If you have not created these roles yet, refer to the documentation here: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-prereqs-self-managed.html.  If you intend to deploy this to more than one child account or are using the CloudFormation StackSet service-managed role, you will need to update the SNS access policy in the management account to include all child account IDs.*

To deploy this template to your preferred AWS Organization child account and region(s) via CloudFormation Stack, please refer to the CloudFormation documentation available at this url: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get started.

* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

