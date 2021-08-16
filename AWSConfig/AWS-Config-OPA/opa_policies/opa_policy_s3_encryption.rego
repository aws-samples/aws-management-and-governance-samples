package s3_bucket_encryption

default compliant = false

compliant = true {
    input.resourceType == "AWS::S3::Bucket"

    any([
    input.supplementaryConfiguration.ServerSideEncryptionConfiguration.rules[_].applyServerSideEncryptionByDefault.sseAlgorithm == "AES256",
    input.supplementaryConfiguration.ServerSideEncryptionConfiguration.rules[_].applyServerSideEncryptionByDefault.sseAlgorithm == "aws:kms"
    ])
}