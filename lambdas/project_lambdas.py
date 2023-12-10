import sys

from aws_cdk import aws_lambda, Duration, aws_iam as iam

from constructs import Construct


LAMBDA_TIMEOUT = 900

BASE_LAMBDA_CONFIG = dict(
    timeout=Duration.seconds(LAMBDA_TIMEOUT),
    memory_size=128,
    tracing=aws_lambda.Tracing.ACTIVE,
)

PYTHON_LAMBDA_CONFIG = dict(
    runtime=aws_lambda.Runtime.PYTHON_3_11, **BASE_LAMBDA_CONFIG
)

from layers import BS4Request


class Lambdas(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        COMMON_LAMBDA_CONF = dict(environment={}, **PYTHON_LAMBDA_CONFIG)
        bs4_requets = BS4Request(self, "BS4")

        self.data_source_creator = aws_lambda.Function(
            self,
            "CR_datasource",
            handler="lambda_function.lambda_handler",
            layers=[bs4_requets.layer],
            code=aws_lambda.Code.from_asset("./lambdas/code/data_source_creator"),
            **COMMON_LAMBDA_CONF
        )

        self.data_source_creator.add_to_role_policy(
            iam.PolicyStatement(actions=["kendra:*"], resources=["*"])
        )

        self.data_source_creator.add_to_role_policy(
            iam.PolicyStatement(actions=["iam:PassRole"], resources=["*"])
        )
