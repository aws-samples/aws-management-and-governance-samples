from aws_cdk import (
    Stack,
    aws_iam as iam, 
    aws_s3 as s3, 
    aws_servicecatalog as sc 
)
from constructs import Construct

class CdkScSampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        #Create a Service Catalog portfolio    
        portfolio = sc.Portfolio(self, 'DevToolsPortfolio',
               display_name='DevTools Portfolio',
               description='Portfolio with approved list of developer tools products',
               provider_name='Central Admin Team')


        #Create a sample Service Catalog product 
        product = sc.CloudFormationProduct(self, "S3SampleStack",
            product_name="S3CDKStack",
            owner="Storage Team",
            product_versions=[
                sc.CloudFormationProductVersion(
                    cloud_formation_template=sc.CloudFormationTemplate.from_product_stack(S3BucketProduct(self, "S3Product")),
                    product_version_name="1.0",
                    description="Deploys an S3 Bucket",
                )
            ])

        tag_options_for_product = sc.TagOptions(self, "ProductTagOptions",
        allowed_values_for_tags={
            "Environment": ["dev", "alpha", "prod"]
            }
        )

        product.associate_tag_options(tag_options_for_product)
        
        # Associate product to the portfolio
        portfolio.add_product(product)


class S3BucketProduct(sc.ProductStack):
         def __init__(self, scope, id):
               super().__init__(scope, id)
               s3.Bucket(self, "ServiceCatalogTestBucket")

