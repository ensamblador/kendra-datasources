#!/usr/bin/env python3
import os

import aws_cdk as cdk

from kendra_datasource.kendra_datasource_stack import KendraDatasourceStack
TAGS = {"app": "generative ai business apps", "customer": "kendra-datasources"}

app = cdk.App()
stk = KendraDatasourceStack(app, "kendra-datasources")
if TAGS.keys():
    for k in TAGS.keys():
        cdk.Tags.of(stk).add(k, TAGS[k])
app.synth()
