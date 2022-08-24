from collections import ChainMap, deque
from contextlib import closing, contextmanager
from contextvars import ContextVar

from src.singleton import singleton


class ContextHandle:
    def __init__(self, **items):
        self.closed = False
        self.items = items
        self.CONTEXT = ChainMap()
        self.CONTEXT.maps = deque([{}])
        self.ACCUMULATED_CONTEXT = {}
        self.CONTEXT.maps.appendleft(items)
        self.ACCUMULATED_CONTEXT.update(items)

    def __iter__(self):
        return iter(self.CONTEXT.items())

    @property
    def context(self):
        return dict(self.CONTEXT)

    @property
    def accumulated_context(self):
        return self.ACCUMULATED_CONTEXT.copy()

    @property
    def context_stack(self):
        return deque(self.CONTEXT.maps)

    def add(self, **items):
        self.items.update(items)

    def remove(self, *keys):
        for key in keys:
            self.items.pop(key, None)

    def reset_accumulated_context(self):
        try:
            return self.ACCUMULATED_CONTEXT
        finally:
            self.ACCUMULATED_CONTEXT = {}

    def close(self):
        if self.closed:
            raise RuntimeError("ContextHandle already closed")

        self.CONTEXT.maps.popleft()
        self.closed = True

        return self.reset_accumulated_context()


@singleton
class GlobalContextHandle(ContextHandle):
    pass


@contextmanager
def context(**items):
    with closing(GlobalContextHandle(**items)) as handle:
        handle.add(**items)
        yield handle


request_context: ContextVar[GlobalContextHandle] = ContextVar("context_handle")
