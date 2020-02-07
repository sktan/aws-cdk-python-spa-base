# Sktan AWS CDK Base Stack - Single Page Application Base

This base stack is designed to provide the bare minimum requirements required to support a serverless single page application styled website on AWS.

## Resources Created

- Cloudfront Distribution
- Website Assets S3 Bucket
- Staging Deployment S3 Bucket
- Lambda Function (to copy assets from the staging s3 bucket to the website assets bucket)

## Prerequisites

- Python 3.6+ and pip
- sktan_cdk.single_page_app

```
pip install sktan-cdk.single-page-app
```

## Deploying as is

If you want to use the stack as is, you will be able to use this like any other CDK stack and then run `cdk synth` to view your results:

### Folder Structure
```
example-spa-website
|-- app.py
|-- cdk.json
|-- website_html
|   |-- index.html
|   |-- css
|   |   |-- example.css
|   |-- images
|   |   |-- logo.jpg
```

### app.py
```
from aws_cdk import core
import sktan_cdk.single_page_app

app = core.App()

spa_app = single_page_app(app, "example-spa-website", website_identifier='www-example-com')
spa_app.create_website_bucket('website_html')
spa_app.create_cloudfront_distribution(cloudfront_alias={
  'acm_cert_ref': 'arn:aws:acm:us-east-1:123456789012:certificate/example-certificate-arn-format',
  'names': [
    'www.example.com'
  ]
})
app.synth()
```

## Extending the stack

If you'd like to use this stack as a basis for your application, then you are free to extend it to implement additional functionality.

```
import sktan_cdk.single_page_app
from aws_cdk import (
  aws_s3 as s3
)

class existing_s3_bucket_website(single_page_app):
  def create_website_bucket(self, deployment_path: typing.Optional[str]):
    s3.fromBucketArn(self, self.__website_identifier, 'arn:aws:s3:::www-example-com')
```
