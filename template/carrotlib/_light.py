import raylib as rl
from typing import TypeVar, TYPE_CHECKING
from linalg import vec2, mat3x3
from _carrotlib import _bake_global_light, _bake_point_light

from ._colors import Colors
from ._node import Node
from . import g as _g

T = TypeVar('T', bound='Light2D')

class Lightmap:
    def __init__(self, width: int, height: int) -> None:
        self.image = rl.GenImageColor(width, height, Colors.Blank)
        rl.ImageFormat(self.image.addr(), rl.PIXELFORMAT_UNCOMPRESSED_R32G32B32A32)
        self.texture = rl.LoadTextureFromImage(self.image)
        # lights
        self.lights = []

    def update(self):
        rl.ImageClearBackground(self.image.addr(), Colors.Black)
        for light in self.lights:
            light._bake(self.image)
        rl.UpdateTexture(self.texture, self.image.data)

    def destroy(self):
        rl.UnloadTexture(self.texture)
        rl.UnloadImage(self.image)

class Light2D(Node):
    color: rl.Color = Colors.White
    intensity: float = 1.0

    def __init__(self, lightmap: Lightmap = None, name=None, parent=None) -> None:
        super().__init__(name=name, parent=parent)
        self.lightmap = lightmap or _g.default_lightmap
        self.lightmap.lights.append(self)

    def _bake(self, image: rl.Image) -> None:
        raise NotImplementedError
    
    def on_destroy(self):
        try:
            self.lightmap.lights.remove(self)
        except ValueError:
            pass


class GlobalLight2D(Light2D):
    def _bake(self, image: rl.Image) -> None:
        _bake_global_light(image.addr(), self.color, self.intensity)


class PointLight2D(Light2D):
    radius: int = 1

    def _bake(self, image: rl.Image) -> None:
        screen_pos = _g.world_to_viewport.transform_point(self.global_position)
        x, y = round(screen_pos.x), round(screen_pos.y)
        _bake_point_light(image.addr(), self.color, self.intensity, x, y, self.radius)


if TYPE_CHECKING:
    from .nodes.particles import Particles


class ParticleLight2D(Light2D):
    parent: 'Particles'
    radius: int = 1

    def _bake(self, image: rl.Image) -> None:
        t = mat3x3.identity()
        for p in self.parent._particles:
            t.copy_trs_(p.position, p.rotation, p.scale)
            p._init_t.matmul(t, out=t)
            screen_pos = _g.world_to_viewport.transform_point(t._t())
            x, y = round(screen_pos.x), round(screen_pos.y)

            color = rl.Color(
                self.color.r * p.color.r // 255,
                self.color.g * p.color.g // 255,
                self.color.b * p.color.b // 255,
                p.color.a
            )
            scale_ratio = t._s().length() / p._init_t._s().length()
            radius = round(self.radius * scale_ratio)
            intensity = color.a / 255 * self.intensity
            _bake_point_light(image.addr(), color, intensity, x, y, radius)