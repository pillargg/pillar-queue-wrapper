import sys
import logging
import uuid

import boto3
from botocore.exceptions import ClientError

class Queue:
    def __init__(self, name, aws_access_key, aws_access_secret, aws_default_region='us-east-1'):
        self.name = name
        self.aws_access_key = aws_access_key,
        self.aws_access_secret = aws_access_secret
        self.aws_default_region = aws_default_region

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(handler)

        self.last_message = None
        self.response = None
        self.fifo = '.fifo' in self.name

        self.sqs_resource = boto3.resource(
            service_name='sqs', 
            region_name=self.aws_default_region,
            aws_access_key_id=self.aws_access_key,
            aws_access_secret_key=self.aws_access_secret
        )
        
        self.queue = self.sqs_resource.get_queue_by_name(QueueName=self.name)

        

    def receive_message(self, wait_time=10):
        """
        Get a message from the queue. `wait_time` is how long it waits before returning `None`.
        """
        try:
            messages = self.queue.receive_message(
                MaxNumberOfMessages=1,
                WaitTimeSeconds=wait_time
            )
        except ClientError as e:
            self.logger.error(e)
            return None
        except Exception as e:
            raise e

        if len(messages) == 1:
            message = messages[0]
            message.delete()
            return message
        
        return None
        
    def wait_for_message(self):
        """
        Blocking function that waits for a message to appear in the specified(via init function) queue. 
        
        Returns the single message that it received from the queue.
        """


        self.logger.info('Waiting for queue item.')
        message = None
        while message is None:
            message = self.receive_message()
        return message

    def send_message(self, message, message_attributes={}, queue_name=None):
        queue = None
        if queue_name is None:
            queue = self.queue
        else:
            queue = self.sqs_resource.get_queue_by_name(QueueName=queue_name)
        
        try:
            if self.fifo:
                self.response = queue.send_message(
                    MessageBody=message,
                    MessageAttributes=message_attributes,
                    MessageDeduplicationId=uuid.uuid1().hex
                )
            else:
                self.response = queue.send_message(
                    MessageBody=message,
                    MessageAttributes=message_attributes
                )
        except ClientError as e:
            self.logger.error(e)
            return False
        except Exception as e:
            raise e

        return True
