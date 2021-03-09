from typing import List, Callable

from pillar_queue.client import Queue
from pillar_queue.lib import get_queue

__name__ = 'queue'

__all__: List[Callable] = [Queue, get_queue]
