from linalg import *
import raylib as rl

from ._colors import Colors
from . import g as _g

Texture2D = rl.Texture2D

class SubTexture2D:
    def __init__(self, main_tex: rl.Texture2D, src_x: int, src_y: int, width: int, height: int):
        self.main_tex = main_tex
        self.src_x = src_x
        self.src_y = src_y
        self.width = width
        self.height = height

def draw_texture(transform: mat3x3, tex: rl.Texture2D, src_rect: rl.Rectangle=None, flip_x=False, flip_y=False, color: rl.Color = None, origin: vec2 = None):
    if _g.is_rendering_ui:
        pos = transform._t()
        rot = transform._r()
        scale = transform._s()
    else:
        transform = _g.world_to_viewport @ transform
        pos = transform._t()
        rot = transform._r()
        scale = transform._s() / _g.PIXEL_PER_UNIT

    src_rect = src_rect or rl.Rectangle(0, 0, tex.width, tex.height)

    dest_width = src_rect.width * scale.x
    dest_height = src_rect.height * scale.y

    if flip_x:
        src_rect.width *= -1
    if flip_y:
        src_rect.height *= -1

    if origin is None:
        origin = vec2(0.5*dest_width, 0.5*dest_height)
    else:
        origin = vec2(origin.x*dest_width, origin.y*dest_height)

    dest_rect = rl.Rectangle(pos.x, pos.y, dest_width, dest_height)
    rl.DrawTexturePro(
        tex,
        src_rect,
        dest_rect,
        origin,
        rot * 57.2957795,       # convert rad to deg
        color or Colors.White,
    )

def draw_text_pro(font: rl.Font, pos: vec2, text: str, font_size: int, spacing: int, line_spacing: int, color: rl.Color, origin: vec2 = None):
    """draw text in world space"""
    if not _g.is_rendering_ui:
        trans = _g.world_to_viewport
        pos = trans.transform_point(pos)
    origin = origin or vec2(0.5, 0.5)
    rl.SetTextLineSpacing(line_spacing + font_size)
    size = rl.MeasureTextEx(font, text, font_size, spacing)
    pos.x -= size.x * origin.x
    pos.y -= size.y * origin.y
    rl.DrawTextEx(font, text, pos, font_size, spacing, color)

def draw_text(pos: vec2, text: str, font_size: int, color: rl.Color):
    """draw text in world space"""
    if not _g.is_rendering_ui:
        trans = _g.world_to_viewport
        pos = trans.transform_point(pos)
    rl.SetTextLineSpacing(font_size)
    width = rl.MeasureText(text, font_size)
    pos.x -= width / 2
    pos.y -= font_size / 2
    rl.DrawText(text, int(pos.x), int(pos.y), font_size, color)

def draw_circle(center: vec2, radius: float, color: rl.Color, solid=True):
    if not _g.is_rendering_ui:
        trans = _g.world_to_viewport
        center = trans.transform_point(center)
        radius *= trans._s().x
    if solid:
        rl.DrawCircle(int(center.x), int(center.y), radius, color)
    else:
        rl.DrawCircleLines(int(center.x), int(center.y), radius, color)


def draw_rect(rect: rl.Rectangle, color: rl.Color = None, origin: vec2 = None, solid=True):
    if not _g.is_rendering_ui:
        rect = rect.copy()
        trans = _g.world_to_viewport
        center = trans.transform_point(vec2(rect.x, rect.y))
        rect.x = center.x
        rect.y = center.y
        scale = trans._s()
        rect.width *= scale.x
        rect.height *= scale.y
    origin = origin or vec2(0.5, 0.5)
    offset_x = rect.width * (0 - origin.x)
    offset_y = rect.height * (0 - origin.y)
    if solid:
        rl.DrawRectangle(
            int(rect.x + offset_x),
            int(rect.y + offset_y),
            int(rect.width),
            int(rect.height),
            color or Colors.White,
        )
    else:
        rl.DrawRectangleLines(
            int(rect.x + offset_x),
            int(rect.y + offset_y),
            int(rect.width),
            int(rect.height),
            color or Colors.White,
        )

def draw_line(begin: vec2, end: vec2, color: rl.Color):
    if not _g.is_rendering_ui:
        trans = _g.world_to_viewport
        begin = trans.transform_point(begin)
        end = trans.transform_point(end)
    rl.DrawLineEx(begin, end, 1, color)

class DebugDraw:
    def draw_polygon(self, vertices: list[vec2], color: vec4):
        trans = _g.world_to_viewport
        vertices = [trans.transform_point(v) for v in vertices]
        vertices.append(vertices[0])
        for i in range(len(vertices) - 1):
            _0 = vertices[i]
            _1 = vertices[i+1]
            rl.DrawLine(int(_0.x), int(_0.y), int(_1.x), int(_1.y), rl.ColorFromNormalized(color))

    def draw_solid_polygon(self, vertices: list[vec2], color: vec4):
        self.draw_polygon(vertices, color)

    def draw_circle(self, center: vec2, radius: float, color: vec4):
        draw_circle(center, radius, rl.ColorFromNormalized(color), solid=False)

    def draw_solid_circle(self, center: vec2, radius: float, axis: vec2, color: vec4):
        draw_circle(center, radius, rl.ColorFromNormalized(color), solid=False)

    def draw_segment(self, p1: vec2, p2: vec2, color: vec4):
        trans = _g.world_to_viewport
        p1 = trans.transform_point(p1)
        p2 = trans.transform_point(p2)
        rl.DrawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y), rl.ColorFromNormalized(color))

    def draw_transform(self, position: vec2, rotation: float):
        pass

    def draw_point(self, p: vec2, size: float, color: vec4):
        pass