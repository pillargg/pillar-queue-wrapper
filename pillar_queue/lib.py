import os

from pillar_queue import Queue


def get_queue(name, aws_access_key=None, aws_access_secret=None):
    '''
    Shortcut function to get a queue. If the queue does not exist on AWS it will throw an error.
    '''

    if aws_access_key is None:
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')

    if aws_access_secret is None:
        aws_access_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')

    q = Queue(
        name=name,
        aws_access_key=aws_access_key,
        aws_access_secret=aws_access_secret
    )

    return q
