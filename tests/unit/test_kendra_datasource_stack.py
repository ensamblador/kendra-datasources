import aws_cdk as core
import aws_cdk.assertions as assertions

from kendra_datasource.kendra_datasource_stack import KendraDatasourceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in kendra_datasource/kendra_datasource_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = KendraDatasourceStack(app, "kendra-datasource")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
