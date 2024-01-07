from linalg import vec2, mat3x3

import raylib as rl

from . import g as _g

class SpriteFont:
    def __init__(self, texture: rl.Texture2D, n_rows: int, n_cols: int, string: str) -> None:
        self.texture = texture
        assert texture.width % n_cols == 0
        assert texture.height % n_rows == 0
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cell_width = texture.width // n_cols
        self.cell_height = texture.height // n_rows
        # bake the font
        self._mapping = {}
        for index, c in enumerate(string):
            src_x = (index % n_cols) * self.cell_width
            src_y = (index // n_cols) * self.cell_height
            self._mapping[c] = src_x, src_y

    def draw(self, transform: mat3x3, string: str, spacing=0, color: rl.Color = None):
        if len(string) == 0:
            return

        scale = transform._s()      # get scale first
        if not _g.is_rendering_ui:
            transform = _g.world_to_viewport @ transform
        pos = transform._t()        # screen position

        dest_width = self.cell_width * scale.x
        dest_height = self.cell_height * scale.y
        spacing *= scale.x

        # calculate total width
        total_width = -spacing
        for c in string:
            total_width += dest_width + spacing

        for c in string:
            src_x, src_y = self._mapping[c]
            src_rect = rl.Rectangle(src_x, src_y, self.cell_width, self.cell_height) 
            dest_rect = rl.Rectangle(
                pos.x - total_width / 2,
                pos.y - dest_height / 2,
                dest_width,
                dest_height,
            )
            color = color or rl.Color(255, 255, 255, 255)
            rl.DrawTexturePro(self.texture, src_rect, dest_rect, vec2(0, 0), 0, color)
            pos.x += dest_width + spacing
