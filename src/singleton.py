def singleton(wrapped):
    class wrapper(wrapped):
        __instance = None
        __initialized = False

        def __new__(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = super().__new__(cls)
            return cls.__instance

        def __init__(self, *args, **kwargs):
            if not self.__initialized:
                super().__init__(*args, **kwargs)
            self.__initialized = True

        @classmethod
        def singleton_reset_(cls):
            cls.__instance = None
            cls.__initialized = False

    wrapper.__module__ = wrapped.__module__
    wrapper.__name__ = wrapped.__name__
    if hasattr(wrapped, "__qualname__"):
        wrapped.__qualname__ = wrapped.__qualname__

    return wrapper
