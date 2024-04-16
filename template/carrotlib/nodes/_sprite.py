import raylib as rl
from linalg import vec2

from .._node import Node
from .. import g as _g
from .._renderer import draw_texture, Texture2D, SubTexture2D
from .._colors import Colors

class Sprite(Node):
    texture: Texture2D | SubTexture2D | None

    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.texture = None
        self.flip_x = False
        self.flip_y = False
        self.origin = vec2(0.5, 0.5)
        self.color = Colors.White.copy()
        self.material = _g.default_material

    def global_rect(self) -> rl.Rectangle:
        """Get the global bounding rectangle of the sprite."""
        if self.texture is None:
            return rl.Rectangle(0, 0, 0, 0)

        trans = self.transform()
        pos = trans._t()
        scale = trans._s() / _g.PIXEL_PER_UNIT
        dest_width = self.texture.width * scale.x
        dest_height = self.texture.height * scale.y

        return rl.Rectangle(
            pos.x - dest_width * self.origin.x,
            pos.y - dest_height * self.origin.y,
            dest_width,
            dest_height
        )

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
