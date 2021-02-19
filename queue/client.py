

import boto3
from botocore.exceptions import ClientError

class Queue:
    def __init__(self, name):
        self.name = name