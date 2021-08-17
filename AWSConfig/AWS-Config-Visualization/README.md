<p align="center">
</p>

## AWS SSM Automation Runbook to Setup AWS Config with Amazon Athena and Amazon QuickSights
This solution is based on the blog [Visualizing AWS Config data using Amazon Athena and Amazon QuickSight](https://aws.amazon.com/blogs/mt/visualizing-aws-config-data-using-amazon-athena-and-amazon-quicksight/).

### What does this cloudformation template do?
This template will deploy a SSM Automation runbook called **Config-QuickSight-Visualization** that can be used to setup AWS Config to be used with Amazon Athena and setup Amazon Quicksights to be able to create visualize dashboards

## Running the Config-QuickSight-Visualization Automation Runbook

### Prerequisite
1.  Configure [Delivering Configuration Snapshot to an Amazon S3 Bucket](https://docs.aws.amazon.com/config/latest/developerguide/deliver-snapshot-cli.html) for AWS.
1.  Ensure access to your S3 Bucket that is used for AWS Config.
1.  The S3 Bucket Name used with AWS Config.
1.  [Amazon Quicksight Subscription](https://docs.aws.amazon.com/quicksight/latest/user/signing-up.html) enabled in your AWS Account.
1.  Authorize [Amazon QuickSight access](https://docs.aws.amazon.com/quicksight/latest/user/athena.html) to the S3 bucket Athena will be using for AWS Config under Security and Permissions within Amazon Quicksights.
1.  The Amazon Quicksight Username.

### Input Parameters for the Config-QuickSight-Visualization Automation Runbook
* **ConfigDeliveryChannelName:** (Required) Name of your AWS Config Delievery Channel.  The default is set to the value of default.
* **ConfigS3BucketLocation:** (Required) AWS Config S3 Bucket Name, this is the name of your S3 Bucket you currently use for AWS Config. (ie config-bucket-1234567891)
* **QuickSightUserName:** (Required) The Amazon QuickSight Username.
* **AutomationAssumeRole:** (Optional) The ARN of the role that allows Automation to perform the actions on your behalf.
* **DeleteConfigVisualization:** (Optional) Set this to true if you would like to delete the resources created to enable this solution. The default is set to false which will setup the solution. 

## Creating Visuals in Amazon QuickSight

The **Config-QuickSight-Visualization** Automation Runbook will create the below views and datasets within Amazon Athena and Amazon QuickSight.  You can then use these to create your visualization dashboard.

*   v_config_rules_compliance
*   v_config_resource_compliance
*   v_config_rds_dbinstances
*   v_config_iam_resources
*   v_config_ec2_vpcs
*   v_config_ec2_instances
*   v_config_resources

#### Creating your Analyses in Amazon QuickSight

1.  From Amazon QuickSight, choose **New analysis**. 
1.  On the **Datasets** page, choose the **v_config_resource_compliance** data set and then choose **Create Analysis**.

#### Create a Visual By Using AutoGraph 

1.  Create a visual by using AutoGraph, which is selected by default.
1.  On the analysis page, choose **accountid** and **compliancetype** in the Fields list pane. 
1.  Amazon QuickSight creates a **Horizontal bar chart** using this data.

#### Adding Additional Datasets to your Analyses

1.  You can add more data sets to the analysis to create more visuals.
1.  From within the analysis, click the **Add,edit,replace and remove datasets** icon.
1.  Click **Add Datasets**.
1.  Select the **v_config_rules_compliance** and click **Select**
1.  In the **Visual types** pane, choose the **Vertical Bar Chart** icon. 
1.  On the analysis page, choose **configrulename** and **compliancetype** in the Fields list pane.
1.  You can create a filter on any field in the currently selected visual. When you create a filter, it applies by default to the currently selected visual only.
1.  Click on the **Filter** icon within the Amazon QuickSight side bar.
1.  Under the Filters section click "**Create one...**" and select the **configrulename** field.
1.  Click on the **configrulename** field and uncheck the **Select all** check box.
1.  Select a couple of Config Rules you would like to dispaly in your visual and clikc **Apply**.
1.  You can then click on the **Visualize** button on the side bar to return to make changes to your visual.

#### Create a Dashboard

1.  In the analysis, choose **Share** in the application bar at upper-right, and then choose **Publish dashboard**. 
1.  In the **Publish dashboard** page that opens, choose **Publish new dashboard as**, and enter the name **Config Dashboard**. 
1.  Choose **Publish dashboard**. 
1.  On the **Share dashboard** page that opens, choose the **X** icon to close it.
