# AWS Config dsl Custom Rule

## This repo contains:
* [Cloudformation templates](./cfn_templates/) which create:
    * a Lambda function for evaluating OPA policies, a Lambda layer containing the [OPA engine](https://www.openpolicyagent.org/docs/latest/), and the proper IAM permissions -> [template](./cfn_templates/lambda_backend/opa-lambda.yaml)
    * a custom Config rule backed by the above Lambda function, and triggered by S3 bucket changes and cheking encryption status -> [template](./cfn_templates/config_rules/opa-s3-encryption.yaml)
    * a custom Config rule backed by the above Lambda function, and triggered by EBS changes and cheking encryption status -> [template](./cfn_templates/config_rules/opa-ebs-encryption.yaml)
    * a custom Config rule backed by the above Lambda function, and triggered by EBS changes and checking attachment status -> [template](./cfn_templates/config_rules/opa-ebs-attachment.yaml)
    * a custom Config rule backed by the above Lambda function, and triggered by Elastic IP changes and checking attachment status -> [template](./cfn_templates/config_rules/opa-eip-attachment.yaml)
  

* Source code for Lambda function and layers:
    * [Lambda function code](./lambda_sources/function/opa_lambda.py) -> `opa_lambda.py`
    * [Lambda function dependencies](./lambda_sources/function/lambda_requirements.txt) to be installed using `pip` -> `lambda_requirements.txt`. Currently, there are no dependencies.
    * [packaged assets](./lambda_sources/packaged_lambda_assets/) -> archived assets already prepared to be uploaded in S3. They contain the Lambda function.
  
  
* [OPA policy files](./opa_policies/) written in [REGO](https://www.openpolicyagent.org/docs/latest/policy-language/) language, needed by the OPA engine to perform evaluations:
    * [opa_policy_s3_encryption](./opa_policies/opa_policy_s3_encryption.rego) evaluates an S3 bucket as `COMPLIANT` only if encryption at rest is enabled
    * [opa_policy_ebs_encryption](./opa_policies/opa_policy_ebs_encryption.rego) evaluates an EBS volume bucket as `COMPLIANT` only if encryption at rest is enabled
  

* [package_lambda.sh](./package_lambda.sh) -> packages all the Lambda function and layer assets into .zip archives and places them in [packaged_lambda_assets](./lambda_sources/packaged_lambda_assets/) folder.



## Deployment Instructions

* Download [OPA engine binary](https://www.openpolicyagent.org/docs/latest/#running-opa) and copy it in [aws-config-dsl-custom-rule/lambda_sources/layers/opa/bin](./lambda_sources/layers/opa/bin)

*  Change directory to [aws-config-dsl-custom-rule/lambda_sources/layers](./lambda_sources/layers) directory, ZIP the entire content, and COPY the zip file to [aws-config-dsl-custom-rule/lambda_sources/packaged_lambda_assets/](./lambda_sources/packaged_lambda_assets/) folder. 
   
*  [**OPTIONAL**] From [aws-config-dsl-custom-rule](./) directory run `./package.sh` -> this will create the Lambda assets in the [packaged_lambda_assets](./lambda_sources/packaged_lambda_assets/) folder. **By default the assets are already in the folder and this step can be skipped if no modifications were made to the Lambda source code or Lambda layer.**
  

* Create or use an existing S3 bucket for storing the Lambda source code and OPA policy files needed (e.g. `<your-bucket-name>`)


* Upload the content of [packaged_lambda_assets](./lambda_sources/packaged_lambda_assets/) into an S3 folder named `packaged_lambda_assets`:
    * `sources.zip` -> `<your-bucket-name>/packaged_lambda_assets/sources.zip`
    * `opa.zip` -> `<your-bucket-name>/packaged_lambda_assets/opa.zip`
    

* Upload the content of [opa_policies](./opa_policies/) into an S3 folder named `opa_policies`:
    * `opa_policy_s3_encrytion.rego` -> `<your-bucket-name>/opa_policies/opa_policy_s3_encrytion.rego`
    * `opa_policy_ebs_encrytion.rego` -> `<your-bucket-name>/opa_policies/opa_policy_ebs_encrytion.rego`
    * `opa_policy_ebs_attachment.rego` -> `<your-bucket-name>/opa_policies/opa_policy_ebs_attachment.rego`
    * `opa_policy_eip_attachment.rego` -> `<your-bucket-name>/opa_policies/opa_policy_eip_attachment.rego`
    * etc...
  

* Deploy [opa-lambda.yaml](./cfn_templates/lambda_backend/opa-lambda.yaml) using [Cloudformation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html). This will create the Lambda backend function that will evaluate your OPA policies and will be triggered by your Config rules:
    * use `<your-bucket-name>` for the `AssetsBucket` parameter
    * use the default values for all the other parameters
  

* After Lambda stack creation finished, deploy which template/s you need from the [config_rules](./cfn_templates/config_rules) folder using [Cloudformation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html). Each tempalte will create one Config rule, that will use one OPA policy and trigger the Lambda function evaluation based on AWS resource configuration change:
    * use `<your-bucket-name>` for the `AssetsBucket` parameter
    * for `ConfigRuleScope` parameter use an AWS resource type, or a comma delimited list or resource types for the scope of the Config rule (e.g. `AWS::EC2::Instance, AWS::S3::Bucket`)
    * use the default values for all the other parameters
  

* After the Config rule stack deployment finished, get the name of Config rule from the ouput `ConfigRuleName` and open Config service console:
    * Based on the [S3 encryption OPA policy](./opa_policies/opa_policy_s3_encryption.rego) we created, the [S3 encryption config Rule](./cfn_templates/config_rules/opa-s3-encryption.yaml) should find all your S3 buckets that have encryption at rest as `COMPLIANT` and the unencrypted buckets as `NON_COMPLIANT`
    * Based on the [EBS encryption OPA policy](./opa_policies/opa_policy_ebs_encryption.rego) we created, the [EBS encryption config Rule](./cfn_templates/config_rules/opa-ebs-encryption.yaml) should find all your EBS volumes that have encryption at rest as `COMPLIANT` and the unencrypted volumes as `NON_COMPLIANT`
    * Based on the [EBS attachment OPA policy](./opa_policies/opa_policy_ebs_attachment.rego) we created, the [EBS attachment config Rule](./cfn_templates/config_rules/opa-ebs-attachment.yaml) should find all your EBS volumes that are attached to an EC2 instance as `COMPLIANT` and the detached volumes as `NON_COMPLIANT`
    * Based on the [EIP attachment OPA policy](./opa_policies/opa_policy_eip_attachment.rego) we created, the [EIP attachment config Rule](./cfn_templates/config_rules/opa-eip-attachment.yaml) should find all your Elastic IPs that are attached to a network interface `COMPLIANT` and the detached Elastic IPs as `NON_COMPLIANT`