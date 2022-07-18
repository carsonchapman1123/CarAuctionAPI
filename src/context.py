from collections import ChainMap, deque
from contextlib import asynccontextmanager, closing


class ContextHandle:
    def __init__(self, **items):
        self.closed = False
        self.items = items
        self.CONTEXT = ChainMap()
        self.CONTEXT.maps = deque([{}])
        self.ACCUMULATED_CONTEXT = {}
        self.CONTEXT.maps.appendleft(items)
        self.ACCUMULATED_CONTEXT.update(items)

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

    def close(self):
        if self.closed:
            raise RuntimeError("ContextHandle already closed")

        self.CONTEXT.maps.popleft()
        self.closed = True

        return {}


@asynccontextmanager
def context(**items):
    with closing(ContextHandle(**items)) as handle:
        yield handle
