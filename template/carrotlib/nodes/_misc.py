import raylib as rl
from linalg import vec2

from .._node import Node
from .._viewport import get_mouse_delta
from .. import g as _g
from .._renderer import draw_texture, Texture2D, SubTexture2D, draw_line
from .._colors import Colors

class FreeCamera(Node):
    def on_update(self):
        # move via mouse wheel button
        if rl.IsMouseButtonDown(rl.MOUSE_BUTTON_MIDDLE):
            delta = get_mouse_delta() / _g.PIXEL_PER_UNIT
            delta.x *= self.scale.x
            delta.y *= self.scale.y
            self.position -= delta

        # zoom via mouse wheel
        zoom = rl.GetMouseWheelMove()
        if zoom != 0:
            self.scale /= 1 + zoom * 5 / _g.PIXEL_PER_UNIT

        _g.world_to_camera.copy_(~self.transform())

class Sprite(Node):
    texture: Texture2D | SubTexture2D | None

    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.texture = None
        self.flip_x = False
        self.flip_y = False
        self.origin = vec2(0.5, 0.5)
        self.color = Colors.White
        self.material = _g.default_material

    def on_render(self):
        if self.texture is None:
            return
        
        if type(self.texture) is Texture2D:
            main_tex = self.texture
            src_rect = None
        elif type(self.texture) is SubTexture2D:
            main_tex = self.texture.main_tex
            src_rect = rl.Rectangle(
                self.texture.src_x, self.texture.src_y,
                self.texture.width, self.texture.height,
            )
        else:
            raise ValueError(f'Unknown texture type: {type(self.texture)}')

        with self.material:
            draw_texture(
                self.transform(),
                main_tex,
                src_rect,
                self.flip_x,
                self.flip_y,
                self.color,
                self.origin
            )


class Grid(Node):
    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.color = rl.Color(255, 255, 255, 64)
        self.cell_width = 1
        self.cell_height = 1
        self.count = 100

    def on_render(self):
        begin, end = vec2(0, 0), vec2(0, 0)
        for i in range(-self.count, self.count + 1):
            begin.x = i * self.cell_width
            begin.y = -self.count * self.cell_height
            end.x = i * self.cell_width
            end.y = self.count * self.cell_height
            draw_line(begin, end, self.color)

            begin.x = -self.count * self.cell_width
            begin.y = i * self.cell_height
            end.x = self.count * self.cell_width
            end.y = i * self.cell_height
            draw_line(begin, end, self.color)
