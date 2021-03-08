from typing import List, Callable

from pillar_queue.client import Queue
from pillar_queue.lib import create_queue

__name__ = 'queue'

__all__: List[Callable] = [Queue, create_queue]
