import raylib as rl
from typing import TypeVar

from ._colors import Colors
from ._math import clamp

def color_with_intensity(color: rl.Color, intensity: float) -> rl.Color:
    color = color.copy()
    color.r = int(clamp(color.r * intensity, 0, 255))
    color.g = int(clamp(color.g * intensity, 0, 255))
    color.b = int(clamp(color.b * intensity, 0, 255))
    return color

T = TypeVar('T', bound='Light2DBase')

class Lightmap:
    def __init__(self, width: int, height: int) -> None:
        self.image = rl.GenImageColor(width, height, Colors.Blank)
        self.texture = rl.LoadTextureFromImage(self.image)
        # lights
        self.lights = []
    
    def new_point_light(self, x: int, y: int, radius: int) -> 'PointLight2D':
        light = PointLight2D(self)
        light.x = x
        light.y = y
        light.radius = radius
        return light

    def update(self):
        rl.ImageClearBackground(self.image.addr(), Colors.Black)
        for light in self.lights:
            light.draw(self.image)

    def destroy(self):
        rl.UnloadTexture(self.texture)
        rl.UnloadImage(self.image)

class Light2DBase:
    color: rl.Color = Colors.White
    intensity: float = 1.0

    def __init__(self, lightmap: Lightmap) -> None:
        self.lightmap = lightmap
        lightmap.lights.append(self)

    def draw(self, image: rl.Image) -> None:
        raise NotImplementedError
    
    def destroy(self):
        try:
            self.lightmap.lights.remove(self)
        except ValueError:
            pass


class GlobalLight2D(Light2DBase):
    def draw(self, image: rl.Image) -> None:
        # TODO: additive blending
        rl.ImageDrawRectangle(
            image.addr(),
            0,
            0,
            image.width,
            image.height,
            color_with_intensity(self.color, self.intensity)
        )


class PointLight2D(Light2DBase):
    radius: int = 1
    x: int = None
    y: int = None

    def draw(self, image: rl.Image) -> None:
        # aseprite draw circle
        # https://www.aseprite.org/docs/circle/
        # TODO: additive blending
        rl.ImageDrawCircle(
            image.addr(),
            self.x,
            self.y,
            self.radius,
            color_with_intensity(self.color, self.intensity)
        )