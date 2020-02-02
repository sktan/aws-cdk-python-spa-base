""" Stack to create the framework of a SPA website """
import typing
from aws_cdk import (
  core,
  aws_cloudfront as cloudfront,
  aws_s3 as s3,
  aws_s3_deployment as s3_deployment
)

class single_page_app(core.Stack):
  """ Stack to create the framework of a SPA website """
  website_assets_bucket = None
  cloudfront_distro = None
  __website_identifier = None

  def __init__(self, scope: core.Construct,
               id: str, website_identifier: str, **kwargs # pylint: disable=redefined-builtin
              ) -> None:
    r"""Initalise the main SPA stack requirements

    NOTE: website_identifier should follow the convention of
    www-example-com rather than www.example.com to conform with
    characters allowed by Cloudformation Resource Ids

    Args:
      id: Cloudformation Stack Name
      website_identifier: The website identifier (e.g. www-example-com)
    """
    super().__init__(scope, id, **kwargs)
    self.__website_identifier = website_identifier

  def create_website_bucket(self, deployment_path: typing.Optional[str]):
    r"""Creates the S3 buckets required to host the SPA website

    Args:
      deployment_path: The path to the contents of your deployable assets
    """
    self.website_assets_bucket = s3.Bucket(self, self.__website_identifier)
    if deployment_path is not None:
      s3_deployment.BucketDeployment(
        self,
        id=f"{self.__website_identifier}-deploy",
        sources=[
          s3_deployment.Source.asset(deployment_path) # pylint: disable=no-value-for-parameter
        ],
        destination_bucket=self.website_assets_bucket
      )

  def create_cloudfront_distribution(self, cloudfront_alias=typing.Optional[dict]):
    r"""Creates the Cloudfront distribution required to access the SPA website

    The Cloudfront distribution will automatically forward requests to the s3 bucket /index.html
    file and serve that as the default for all HTTP URIs that don't exist so that the index file
    can be served for any dynamic path

    NOTE: If cloudfront_alias is defined, the default `security_policy` is
      aws_cloudfront.SecurityPolicyProtocol.TLS_V1_2_2018 which can be by defining `security_policy`
      in the dictionary if required

    Args:
      cloudfront_alias: Aliases your Cloudfront distribution should use and should
        include a dictionary containing array(`names`) and str(`acm_cert_ref`)
    """
    cloudfront_originaccesspolicy = cloudfront.OriginAccessIdentity(
      self,
      f"{self.__website_identifier}-originpolicy",
    )
    alias_configuration = None
    if cloudfront_alias is not None:
      if 'security_policy' not in cloudfront_alias:
        cloudfront_alias['security_policy'] = cloudfront.SecurityPolicyProtocol.TLS_V1_2_2018
      cloudfront_alias = cloudfront.AliasConfiguration(**cloudfront_alias)
    self.cloudfront_distro = cloudfront.CloudFrontWebDistribution(
      self,
      id=f"{self.__website_identifier}-cloudfront",
      price_class=cloudfront.PriceClass.PRICE_CLASS_ALL,
      alias_configuration=alias_configuration,
      origin_configs=[
        cloudfront.SourceConfiguration(
          behaviors=[
            cloudfront.Behavior(is_default_behavior=True)
          ],
          s3_origin_source=cloudfront.S3OriginConfig(
            s3_bucket_source=self.website_assets_bucket,
            origin_access_identity=cloudfront_originaccesspolicy
          )
        )
      ],
      error_configurations=[
        cloudfront.CfnDistribution.CustomErrorResponseProperty(
          error_code=404,
          error_caching_min_ttl=0,
          response_code=200,
          response_page_path="/index.html"
        )
      ]
    )
