import raylib as rl
from _carrotlib import list_assets
from typing import Iterable, Literal

from ._resources import load_texture
from ._renderer import Texture2D, SubTexture2D

LoopType = Literal['forward', 'ping-pong'] | None

class FramedAnimation:
    def __init__(self, frames: list[Texture2D | SubTexture2D], speed: int, loop: LoopType):
        self.frames = frames
        self.speed = speed
        self.loop = loop

        if self.loop == 'ping-pong':
            self.frames += self.frames[-2:0:-1]

def load_framed_animation(path: str, speed: int, loop: LoopType = None):
    frames = []
    for frame in sorted(list_assets(path)):
        frames.append(load_texture(frame))
    return FramedAnimation(frames, speed, loop)

def load_framed_animation_atlas(path: str, tile_width: int, tile_height: int, tile_indices: Iterable[int], speed: int, loop: LoopType = None):
    main_tex = load_texture(path)
    assert main_tex.width % tile_width == 0
    assert main_tex.height % tile_height == 0
    frames = []
    tiles_per_row = main_tex.width // tile_width
    for i in tile_indices:
        src_x = (i % tiles_per_row) * tile_width
        src_y = (i // tiles_per_row) * tile_height
        frames.append(SubTexture2D(main_tex, src_x, src_y, tile_width, tile_height))
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

    def update(self) -> Texture2D | SubTexture2D | None:
        if self._current_animation is None:
            return

        self._current_frame += self._current_animation.speed * rl.GetFrameTime() * self.speed

        if self._current_frame >= len(self._current_animation.frames):
            if self._current_animation.loop:
                self._current_frame = 0
            else:
                self._current_animation = None
                return
        return self._current_animation.frames[int(self._current_frame)]
