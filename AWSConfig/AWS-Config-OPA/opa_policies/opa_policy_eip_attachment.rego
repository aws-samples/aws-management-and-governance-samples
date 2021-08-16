package eip_attachment

default compliant = false

compliant = true {
    input.resourceType == "AWS::EC2::EIP"
    input.configuration.associationId != null
}