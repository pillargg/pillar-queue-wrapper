import os

import pytest
import concurrent.futures
import time

from pillar_queue import Queue


def delete_all_messages_from_queue(queue):
    while True:
        message = queue.receive_message(wait_time=1)
        if message is None:
            break


def instantiate_queue(name="testqueue.fifo"):
    q = Queue(
        name=name
    )
    delete_all_messages_from_queue(q)
    return q


def insert_message_into_queue_for_testing(queue):
    queue.send_message()


def test_Queue_init():
    q = instantiate_queue()

    delete_all_messages_from_queue(q)

    assert(q.name == "testqueue.fifo")
    assert(q.aws_default_region == 'us-east-1')
    assert(len(q) == 0)


def test_send_message():
    q = instantiate_queue()
    success = q.send_message(message='hello')
    assert success


def test_equals():
    q = instantiate_queue()
    q2 = instantiate_queue()
    assert(q == q2)


def test_receive_message():
    q = instantiate_queue()
    assert(len(q) == 0)

    q.send_message('hello')
    message = q.receive_message(wait_time=1, delete_message=True)
    assert(message)
    assert(message.body == 'hello')
    assert(len(q) == 0)

    q.send_message('hello')
    message = q.receive_message(wait_time=1, delete_message=False)
    assert(message)
    assert(message.body == 'hello')
    assert(q[0] == message)
    assert(len(q) == 1)

    message = q.receive_message(wait_time=1, delete_message=True)
    assert(len(q) == 0)

    start_time = time.perf_counter()
    message = q.receive_message(wait_time=1, delete_message=True)
    time_delta = time.perf_counter() - start_time

    assert(time_delta < 1.5)
    assert(message is None)

    start_time = time.perf_counter()
    message = q.receive_message(wait_time=10, delete_message=True)
    time_delta = time.perf_counter() - start_time

    assert(time_delta > 9 and time_delta < 11)
    assert(message is None)


def test_receive_messages():
    q = instantiate_queue()
    assert(len(q) == 0)

    start_time = time.perf_counter()
    messages = q.receive_messages(
        max_number=10, wait_time=10, delete_messages=True)
    time_delta = time.perf_counter() - start_time
    assert(time_delta > 9 and time_delta < 11)
    assert(messages == [])

    q.send_message('hello')
    start_time = time.perf_counter()
    messages = q.receive_messages(
        max_number=10, wait_time=10, delete_messages=True)
    time_delta = time.perf_counter() - start_time
    assert(time_delta > 9 and time_delta < 11)
    assert(len(messages) == 1)
    assert(messages[0].body == 'hello')
    assert(len(q) == 0)

    q.send_message('hello')
    q.send_message('world')
    start_time = time.perf_counter()
    messages = q.receive_messages(
        max_number=2, wait_time=10, delete_messages=True)
    time_delta = time.perf_counter() - start_time
    assert(time_delta < 1.5)
    assert(len(messages) == 2)
    assert(messages[0].body == 'hello')
    assert(messages[1].body == 'world')
    assert(len(q) == 0)

    for i in range(10):
        q.send_message(i)
    start_time = time.perf_counter()
    messages = q.receive_messages(
        max_number=10, wait_time=10, delete_messages=True)
    time_delta = time.perf_counter() - start_time
    assert(time_delta < 1.5)
    assert(len(messages) == 10)
    for i in range(10):
        assert(messages[i].body == i)
    assert(len(q) == 0)

    for i in range(11):
        q.send_message(i)
    start_time = time.perf_counter()
    messages = q.receive_messages(
        max_number=10, wait_time=10, delete_messages=True)
    time_delta = time.perf_counter() - start_time
    assert(time_delta < 1.5)
    assert(len(messages) == 10)
    for i in range(10):
        assert(messages[i].body == i)
    assert(len(q) == 1)

    for i in range(11):
        q.send_message(i)
    start_time = time.perf_counter()
    messages = q.receive_messages(
        max_number=10, wait_time=10, delete_messages=False)
    time_delta = time.perf_counter() - start_time
    assert(time_delta < 1.5)
    assert(len(messages) == 10)
    for i in range(10):
        assert(messages[i].body == i)
    assert(len(q) == 11)


def test_wait_for_message():
    q = instantiate_queue()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(q.wait_for_message)
        q.send_message(message='hello')
        message = future.result()
        assert(message)
        assert(message.body == 'hello')


def test_num_messages():

    q = instantiate_queue()
    assert(len(q) == 0)

    q.send_message(message='hello')
    time.sleep(1)
    assert(len(q) == 1)

    q.send_message(message='world')
    time.sleep(1)
    assert(len(q) == 2)


@pytest.mark.skip(reason='Takes forever.')
def test_purge():
    q = instantiate_queue()

    # case where queue is empty to begin with
    success = q.purge()
    assert(success)
    assert(len(q) == 0)

    # case where queue is not empty
    q.send_message(message='hello')
    assert(len(q) == 1)

    success = q.purge()
    assert(success)
    assert(len(q) == 0)

    q.send_message(message='hello')
    q.send_message(message='hello')
    assert(len(q) == 2)

    success = q.purge()
    assert(success)
    assert(len(q) == 0)


def is_index_error(q, index):
    try:
        q[index]
        return False
    except IndexError:
        return True
    except Exception as e:
        raise e


def test_getitem():
    q = instantiate_queue(name="testqueue")

    # case where queue is empty
    assert(is_index_error(q, 0))
    assert(is_index_error(q, 1))
    assert(is_index_error(q, -1))

    # case where queue is not empty
    q.send_message(message='hello')
    assert(q[0] != None)
    assert(q[0] != None)
    assert(q[0].body == 'hello')
    assert(is_index_error(q, 1))
    assert(q[-1].body == 'hello')

    q.send_message(message='world')
    assert(q[0] != None)
    assert(q[0].body == 'hello')
    assert(q[1] != None)
    assert(q[1].body == 'world')
    assert(is_index_error(q, 2))
    assert(queue[-1] == 'world')
    assert(queue[-2] == 'hello')


def test_setitem():
    q = instantiate_queue()

    # case where queue is empty
    assert(is_index_error(q, 0))
    q[0] = 'hello'
    assert(q[0].body == 'hello')

    delete_all_messages_from_queue(q)

    assert(is_index_error(q, 0))
    q[1] = 'hello'
    assert(q[0].body == 'hello')
    assert(is_index_error(q, 1))

    delete_all_messages_from_queue(q)

    assert(is_index_error(q, 0))
    q[-1] = 'hello'
    assert(q[0].body == 'hello')
    assert(is_index_error(q, 1))

    delete_all_messages_from_queue(q)

    assert(is_index_error(q, 0))
    q[0] = 'hello'
    q[-1] = 'world'
    assert(q[0].body == 'hello')
    assert(q[1].body == 'world')
    assert(is_index_error(q, 2))

    delete_all_messages_from_queue(q)

    assert(is_index_error(q, 0))
    q[0] = 'hello'
    q[1] = 'world'
    q[0] = 'this should be at the end'
    assert(q[0].body == 'hello')
    assert(q[1].body == 'world')
    assert(q[2].body == 'this should be at the end')
    assert(is_index_error(q, 3))


def test_delitem():
    q = instantiate_queue()

    q.send_message(message='hello')
    del q[0]
    assert(q[0] is None)

    q.send_message(message='hello')
    q.send_message(message='world')
    del q[0]
    assert(q[0].body == 'world')

    delete_all_messages_from_queue(q)

    q.send_message(message='hello')
    q.send_message(message='world')
    del q[1]
    assert(q[0].body == 'hello')
    assert(q[1] is None)

    delete_all_messages_from_queue(q)

    q.send_message(message='hello')
    q.send_message(message='world')
    q.send_message(message='baz')

    del q[1]
    assert(q[0].body == 'hello')
    assert(q[1].body == 'baz')
    assert(q[2] is None)


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
