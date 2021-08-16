package ebs_attachment

default compliant = false

compliant = true {
    input.resourceType == "AWS::EC2::Volume"
    count(input.configuration.attachments) > 0
}