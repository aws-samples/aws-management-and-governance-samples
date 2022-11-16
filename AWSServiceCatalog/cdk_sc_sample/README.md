## CDK SC Sample Stack - AWS Service Catalog 

This file contains sample code to create an AWS Service Catalog portfolio with a single Service Catalog product.  In this example, the product is a S3 bucket.   You can choose to add more products to this portfolio.   



To deploy, run these commands


```
$ mkdir cdk_sc_sample && cd cdk_sc_sample
$ cdk init app --language=python
$ pip install -r requirements.txt
```

Copy this cdk_sc_sample repo into your cdk_sc_sample directory.  

After this, you can run the following: 

```
$ cdk bootstrap 
$ cdk deploy    
```

This will deploy the Service Catalog portfolio and its product into your account.  