import os

from pillar_queue import Queue

def create_queue(name, aws_access_key=None, aws_access_secret=None):
    '''
    Shortcut function to create a queue
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
