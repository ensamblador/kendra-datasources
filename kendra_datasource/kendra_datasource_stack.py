import boto3
from aws_cdk import (
    # Duration,
    Stack,
    aws_kendra as kendra

)


from kendra_constructs import CRKendraCrawlerV2Datasource, CRKendraS3Datasource, KendraServiceRole

from constructs import Construct
from s3_cloudfront import S3Deploy
from lambdas import Lambdas


class KendraDatasourceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.index_id = self.get_kendra_index()
        self.role = KendraServiceRole(self, "KSR")

        self.Fn = Lambdas(self, "Fn")

        self.s3_files = S3Deploy(self, "files_es","files_es", "files_es")
        self.s3_files.deploy("urls","urls", "s3_urls")
        
        self.create_s3_datasource()
        
        self.create_crawler_datasource()

    def get_kendra_index(self):
        kendra_index_id = self.get_ssm_parameter("kendra-index-id")
        return kendra_index_id
    
    def get_ssm_parameter(self, parameter_name):
        return boto3.client("ssm").get_parameter(Name=f"/gen-ai-apps/{parameter_name}")[
            "Parameter"
        ]["Value"]



    def create_s3_datasource(self):
        CRKendraS3Datasource(
            self,
            "s3_data_files",
            service_token=self.Fn.data_source_creator.function_arn,
            index_id=self.index_id,
            role_arn=self.role.arn,
            name="latam-cambios-devoluciones",
            description="",
            bucket_name=self.s3_files.bucket.bucket_name,
            language_code="es",
            inclusion_prefixes=["files_es/documents/"],
            # metadata_files_prefix = "files_es/metadata/",
            inclusion_patterns=[],
        )

    def create_crawler_datasource(self):
        for i in range(1, 16):
            url_file = f"ml_blogs_{i}.txt"
            s3_seed_url = f"s3://{self.s3_files.bucket.bucket_name}/s3_urls/{url_file}"

            CRKendraCrawlerV2Datasource(
                self,
                f"Blogs{i}",
                service_token=self.Fn.data_source_creator.function_arn,
                index_id=self.index_id,
                role_arn=self.role.arn,
                name=f"machine-learning-blogs-{i*100}",
                seed_urls=None,
                s3_seed_url=s3_seed_url,
                url_inclusion_patterns=["*.aws.amazon.com/blogs/machine-learning/.*"],
                url_exclusion_patterns=["*./tag/.*"],
            )
