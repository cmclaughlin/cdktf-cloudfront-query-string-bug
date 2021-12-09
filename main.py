#!/usr/bin/env python

"""
cloudfront-test
"""

from cdktf_cdktf_provider_aws import AwsProvider
from constructs import Construct

from cdktf import App, TerraformStack


from cdktf_cdktf_provider_aws.cloudfront import (
    CloudfrontDistribution,
    CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies,
    CloudfrontDistributionDefaultCacheBehaviorForwardedValues,
    CloudfrontDistributionDefaultCacheBehavior,
    CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies,
    CloudfrontDistributionOrderedCacheBehaviorForwardedValues,
    CloudfrontDistributionOrderedCacheBehavior,
    CloudfrontDistributionOrigin,
    CloudfrontDistributionOriginCustomOriginConfig,
    CloudfrontDistributionRestrictionsGeoRestriction,
    CloudfrontDistributionRestrictions,
    CloudfrontDistributionViewerCertificate,
)

class MyStack(TerraformStack):
    """
    cloudfront-test
    """

    def __init__(self, scope: Construct, ns: str):

        super().__init__(scope, ns)

        AwsProvider(self, "Aws", region="us-east-1")

        default_cookies = (
            CloudfrontDistributionDefaultCacheBehaviorForwardedValuesCookies(
                forward="none",
            )
        )

        default_forwarded_values = (
            CloudfrontDistributionDefaultCacheBehaviorForwardedValues(
                cookies=default_cookies,
                query_string=False,
                headers=[
                    "Accept",
                    "Host",
                    "Origin",
                    "Referer",
                ],
            )
        )

        default_cache_behavior = CloudfrontDistributionDefaultCacheBehavior(
            allowed_methods=["GET", "HEAD"],
            cached_methods=["GET", "HEAD"],
            forwarded_values=default_forwarded_values,
            target_origin_id="my-target",
            viewer_protocol_policy="allow-all",
        )

        ordered_cookies = (
            CloudfrontDistributionOrderedCacheBehaviorForwardedValuesCookies(
                forward="none",
            )
        )

        ordered_forwarded_values = (
            CloudfrontDistributionOrderedCacheBehaviorForwardedValues(
                cookies=ordered_cookies,
                query_string=False,
            )
        )

        ordered_cache_behavior = [
            CloudfrontDistributionOrderedCacheBehavior(
                forwarded_values=ordered_forwarded_values,
                path_pattern="/xxx",
                target_origin_id="xxx",
                allowed_methods=["GET", "HEAD"],
                cached_methods=["GET", "HEAD"],
                viewer_protocol_policy="allow-all",
            )
        ]

        origins = [
            CloudfrontDistributionOrigin(
                domain_name="xxx",
                origin_id="xxxx",
                custom_origin_config=CloudfrontDistributionOriginCustomOriginConfig(
                    http_port=80,
                    https_port=443,
                    origin_protocol_policy="https-only",
                    origin_ssl_protocols=[
                        "TLSv1",
                        "TLSv1.1",
                        "TLSv1.2",
                    ],
                    origin_keepalive_timeout=5,
                    origin_read_timeout=30,
                ),
            )
        ]

        geo_restriction = CloudfrontDistributionRestrictionsGeoRestriction(
            restriction_type="none",
        )

        restrictions = CloudfrontDistributionRestrictions(
            geo_restriction=geo_restriction,
        )

        viewer_certificate = CloudfrontDistributionViewerCertificate(
            acm_certificate_arn="xxx",
            minimum_protocol_version="TLSv1.2_2018",
            ssl_support_method="sni-only",
        )

        CloudfrontDistribution(
            self,
            "distro",
            aliases=["xxx"],
            comment="xxx",
            default_cache_behavior=default_cache_behavior,
            enabled=True,
            is_ipv6_enabled=True,
            ordered_cache_behavior=ordered_cache_behavior,
            origin=origins,
            restrictions=restrictions,
            viewer_certificate=viewer_certificate,
        )


if __name__ == "__main__":
    app = App()
    stack = MyStack(app, "cloudfront-test")
    app.synth()
