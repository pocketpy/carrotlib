import raylib as rl
from _carrotlib import list_assets
from typing import Iterable

from ._resources import load_texture
from ._renderer import Texture2D, SubTexture2D

class FramedAnimation:
    def __init__(self, frames: list[Texture2D | SubTexture2D], speed: int, loop: bool):
        self.frames = frames
        self.speed = speed
        self.loop = loop

def load_framed_animation(path: str, speed: int, loop: bool):
    frames = []
    for frame in sorted(list_assets(path)):
        frames.append(load_texture(frame))
    return FramedAnimation(frames, speed, loop)

def load_framed_animation_atlas(path: str, tile_size: int, tile_indices: Iterable[int], speed: int, loop: bool):
    main_tex = load_texture(path)
    assert main_tex.width % tile_size == 0
    assert main_tex.height % tile_size == 0
    frames = []
    tiles_per_row = main_tex.width // tile_size
    for i in tile_indices:
        src_x = (i % tiles_per_row) * tile_size
        src_y = (i // tiles_per_row) * tile_size
        frames.append(SubTexture2D(main_tex, src_x, src_y, tile_size, tile_size))
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
        dt = rl.GetFrameTime()
        self._current_frame += self._current_animation.speed * dt * self.speed
        if self._current_frame >= len(self._current_animation.frames):
            if self._current_animation.loop:
                self._current_frame = 0
            else:
                self._current_animation = None
                return
        return self._current_animation.frames[int(self._current_frame)]
