import json
from constructs import Construct

from aws_cdk import (
    aws_lambda as _lambda

)



class BS4Request(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bs4_requests = _lambda.LayerVersion(
            self, "Bs4Requests", code=_lambda.Code.from_asset("./layers/bs4_requests.zip"),
            compatible_runtimes = [_lambda.Runtime.PYTHON_3_10, _lambda.Runtime.PYTHON_3_11, _lambda.Runtime.PYTHON_3_9, _lambda.Runtime.PYTHON_3_8 ], 
            description = 'BeautifulSoup y Requests')

        
        self.layer = bs4_requests