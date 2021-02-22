# pillar-queue-wrapper
Pillar's wrapper around [AWS SQS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html)

There are 2 options for authentication through this wrapper
- Explicit: Where the 'aws_access_key' and 'aws_access_secret' are explicitly passed into the queue function
- Implicit: Where 'None' is passed into the queue function and it trys to get the credetials from the [AWS cli](https://github.com/aws/aws-cli/tree/v2) Install the aws cli and add the 'aws_access_key' and 'aws_access_secret' to it.
## Quickstart/Basic Usage
```python
    q = Queue(
        name="queuename",
        aws_access_key="aws_access_key here",
        aws_access_secret="aws_access_secret here",
        aws_default_region='us-east-1',
    )
    #Note if a queue name ends with .fifo, it is a fifo queue

    q.send_message(message="A test message", message_attributes={}, message_group_id=None, deduplication_id=None)

    #blocking function that will wait for a message to appear
    message = q.wait_for_message(delete_message=True)
    print(message.body)
```

## Testing

1) Install AWS CLI with `pip install awscli`, insert your AWS iam Access key ID and Secret access key found in [the AWS IAM console](https://console.aws.amazon.com/iam/home)

2) Make two queues in the SQS Tab called `testqueue` and `testqueue.fifo`. The queue `testqueue.fifo` should be of the FIFO type detailed [here](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html). These queues will be used to run the tests.

3) Run 'pytest'

## Future Features:
- Queue creation/destruction
- Message pooling
- get,set, and delete functionality to use queues like arrays pythonically
