import os

import pytest

from queue import Queue

def instantiate_queue():
    q = Queue(
        name="testqueue.fifo", 
        aws_access_key=os.environ.get('AWS_ACCESS_KEY_ID'), 
        aws_access_secret=os.environ.get('AWS_ACCESS_SECRET_KEY')
    )
    return q

def insert_message_into_queue_for_testing(queue):
    queue.send_message()


def test_Queue_init():
    q = instantiate_queue()

    assert(q.name == "testqueue.fifo")
    assert(q.last_message is None)
    assert(q.aws_default_region == 'us-east-1')

def test_send_message():
    q = instantiate_queue()
    success = q.send_message(message='hello')
    assert success

def test_wait_for_message():
    q = instantiate_queue()

    message = q.wait_for_message()

    assert(message)

# def chandler_this_isnotatestitishowitwillbeimplementednormally():
#     video_downloader = instantiate_queue()
#     clip_processor = instantiate_queue()
#     while True:
#         message = video_downloader.wait_for_message()
        
#         success = False
#         while trys < 5:
#             success = dostuff()
#             if success:
#                 break
#         if success == False:
#             #also alert in logdna -> put it in failure queue 
#             #put Item back in queue

#         assert(message)

#         clip_processor.send_message('hello')

    


# def test_queueing_integration_event_based():
#     def callback(message,queue):
#         print(message)
#         #processing happens here
#         #processing finishes
#         queue.send_message('done_here_is_the_result','queue_name')
#     q = Queue()
#     q.set_on_message('a_message_here',q)
#     q.start()

# def test_queueing_integration():
#     q = Queue()
#     while True:
#         message = q.wait_for_message()
#         print(message)
#         #processing happens here in internal call like video_downloader.download_video(message)
#         q.send_message('done_here_is_the_result','queue_name')
        
