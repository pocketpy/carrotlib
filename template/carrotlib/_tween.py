import easing
import raylib as rl

from typing import Callable
from __builtins import next

from ._node import Node

class Tween:
    Ready = 0
    Playing = 1
    Completed = 2

    completed: Callable = None

    def __init__(self):
        self._state = Tween.Ready

    @property
    def state(self):
        return self._state
    
    def is_ready(self):
        return self._state == Tween.Ready

    def is_playing(self):
        return self._state == Tween.Playing
    
    def is_completed(self):
        return self._state == Tween.Completed

    def _setup(self):
        if self._state != Tween.Ready:
            raise ValueError("a Tween instance can only be setup once")
        self._state = Tween.Playing

    def play(self, node: Node):
        self._setup()
        node.start_coroutine(self)

    @staticmethod
    def delay(duration: float):
        return _Delayer(duration)


class _Delayer(Tween):
    def __init__(self, duration: float):
        super(_Delayer, self).__init__()
        self.duration = duration

    def _setup(self):
        super(_Delayer, self)._setup()
        self._start_time = rl.GetTime()

    def __next__(self):
        t = rl.GetTime() - self._start_time
        if t >= self.duration:
            self._state = Tween.Completed
            if self.completed is not None:
                self.completed()
            return StopIteration


class Tweener(Tween):
    def __init__(self, obj, name, target, duration, ease=None):
        super(Tweener, self).__init__()
        self.obj = obj                  # target object
        self.name = name                # target attribute name
        self.target = target            # target value
        self.duration = duration        # duration in seconds
        self.ease = ease or easing.OutQuad      # easing function
        assert type(name) is str
    
    def _setup(self):
        super(Tweener, self)._setup()
        self._start_time = rl.GetTime()
        self._start_val = getattr(self.obj, self.name)

    def __next__(self):
        t = rl.GetTime() - self._start_time
        if t >= self.duration:
            setattr(self.obj, self.name, self.target)
            self._state = Tween.Completed
            if self.completed is not None:
                self.completed()
            return StopIteration
        progress = self.ease(t / self.duration)
        curr = self._start_val + (self.target - self._start_val) * progress
        setattr(self.obj, self.name, curr)
        return curr


class TweenList(Tween):
    items: list[Tween]

    def __init__(self):
        super(TweenList, self).__init__()
        self.items = []

    def append(self, tween):
        self.items.append(tween)

    def extend(self, tweens):
        self.items.extend(tweens)

    def _setup(self):
        super(TweenList, self)._setup()
        self._i = 0
        assert len(self.items) > 0
        self.items[0]._setup()

    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, i) -> Tween:
        return self.items[i]

    def __next__(self):
        tween = self.items[self._i]
        if next(tween) is not StopIteration:
            return
        self._i += 1
        if self._i >= len(self.items):
            self._state = Tween.Completed
            if self.completed is not None:
                self.completed()
            return StopIteration
        else:
            self.items[self._i]._setup()
