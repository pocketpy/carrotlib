import raylib as rl
from _carrotlib import list_assets
from ._resources import load_texture

class FramedAnimation:
    def __init__(self, frames: list[rl.Texture2D], speed: int, loop: bool):
        self.frames = frames
        self.speed = speed
        self.loop = loop

def load_framed_animation(path: str, speed: int = 12, loop: bool = True) -> FramedAnimation:
    frames = []
    for frame in sorted(list_assets(path)):
        frames.append(load_texture(frame))
    return FramedAnimation(frames, speed, loop)

class FramedAnimator:
    speed: float
    _animations: dict[str, FramedAnimation]
    _current_animation: FramedAnimation
    _current_frame: float

    def __init__(self):
        self.speed = 1.0
        self._animations = {}
        self._current_animation = None
        self._current_frame = 0

    def __setitem__(self, name: str, anim: FramedAnimation):
        assert isinstance(anim, FramedAnimation)
        self._animations[name] = anim

    def __getitem__(self, name: str) -> FramedAnimation:
        return self._animations[name]

    def play(self, name: str, speed: float = 1.0):
        anim = self._animations[name]
        self.speed = speed
        if anim is self._current_animation:
            return
        self._current_frame = 0
        self._current_animation = anim

    def stop(self):
        self._current_animation = None

    def update(self) -> rl.Texture2D:
        if self._current_animation is None:
            return
        dt = rl.GetFrameTime()
        self._current_frame += self._current_animation.speed * dt * self.speed
        if self._current_frame >= len(self._current_animation.frames):
            if self._current_animation.loop:
                self._current_frame = 0
            else:
                self._current_animation = None
                return
        return self._current_animation.frames[round(self._current_frame)]
