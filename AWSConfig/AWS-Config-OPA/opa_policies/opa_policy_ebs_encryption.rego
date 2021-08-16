package ebs_encryption

default compliant = false

compliant = true {
    input.resourceType == "AWS::EC2::Volume"
    input.configuration.encrypted == true
}