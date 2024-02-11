from typing import Callable, Generic, TypeVar

T = TypeVar('T')

class Event(Generic[T]):
    handlers: list[Callable[[T], None]]

    def __init__(self):
        self.handlers = []

    def __add__(self, handler):
        self.handlers.append(handler)
        return self
    
    def __sub__(self, handler):
        self.handlers.remove(handler)
        return self
    
    def __call__(self, obj: T, **kwargs):
        for handler in self.handlers:
            handler(obj, **kwargs)

    def clear(self):
        self.handlers.clear()
