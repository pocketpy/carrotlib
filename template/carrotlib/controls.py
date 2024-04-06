import raylib as rl
from linalg import vec2
from typing import Literal

from _carrotlib import _rlDrawTextBoxed

from ._node import Node
from ._colors import Colors
from ._font import SpriteFont
from ._renderer import draw_text, draw_rect, Texture2D, SubTexture2D

from . import g as _g

def _convert_coordinates(old_pivot: vec2, new_pivot: vec2, position: vec2, width: float, height: float):
    # 计算旧锚点到新锚点的偏移量
    offset_x = (new_pivot.x - old_pivot.x) * width
    offset_y = (new_pivot.y - old_pivot.y) * height
    # 用偏移量更新向量
    return vec2(position.x - offset_x, position.y - offset_y)


class ButtonState:
    value: Literal['normal', 'hover', 'pressed', 'disabled']

    def __init__(self, control: 'Control', on_click, on_long_press) -> None:
        self.value = 'normal'
        self.control = control
        self.on_click = on_click
        self.on_long_press = on_long_press

        self._pressed_time = None

        self.colors = {
            'normal': Colors.White,
            'hover': Colors.LightGray,
            'pressed': Colors.Gray,
            'disabled': Colors.DarkGray,
        }

    @property
    def color(self) -> rl.Color:
        return self.colors[self.value]

    def update(self):
        old_value = self.value
        if not self.control.interactable:
            self.value = 'disabled'

        if self.value == 'disabled':
            self._pressed_time = None
            if self.control.interactable:
                self.value = 'normal'
        elif self.value == 'normal':
            self._pressed_time = None
            if self.control.is_hovering():
                if rl.IsMouseButtonPressed(0):
                    self.value = 'pressed'
                    self._pressed_time = rl.GetTime()
                else:
                    self.value = 'hover'
        elif self.value == 'hover':
            self._pressed_time = None
            if not self.control.is_hovering():
                self.value = 'normal'
            elif rl.IsMouseButtonPressed(0):
                self.value = 'pressed'
                self._pressed_time = rl.GetTime()
        elif self.value == 'pressed':
            if self.on_long_press and self._pressed_time is not None and rl.GetTime() - self._pressed_time > 0.5:
                if self.control.is_hovering():
                    self.on_long_press()
                    self.value = 'hover'
                self._pressed_time = None
            elif rl.IsMouseButtonReleased(0):
                if self.control.is_hovering():
                    if self.on_click:
                        self.on_click()
                    self.value = 'hover'
                else:
                    self.value = 'normal'
                self._pressed_time = None

        return self.value != old_value


        



class Control(Node):
    parent: 'Control'   # we assume a control's parent is also a control

    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.interactable = False

    def create_button_state(self, on_click=None, on_long_press=None) -> ButtonState:
        return ButtonState(self, on_click, on_long_press)

    def rect(self) -> rl.Rectangle:
        return rl.Rectangle(0, 0, 0, 0)
    
    def is_hovering(self) -> bool:
        return _g.hovered_control is self
    
    def is_pressed(self) -> bool:
        return self.is_hovering() and rl.IsMouseButtonPressed(0)
    
    def is_released(self) -> bool:
        return self.is_hovering() and rl.IsMouseButtonReleased(0)
    
    def set_position(self, position: vec2, pivot: vec2, new_pivot: vec2 = None):
        """Set position based on pivot
        + `(0, 0)`: top left
        + `(0.5, 0.5)`: center
        + `(1, 1)`: bottom right
        """
        rect = self.parent.rect()
        parent_scale = self.parent.transform()._s()
        width = rect.width / parent_scale.x
        height = rect.height / parent_scale.y
        new_pivot = new_pivot or vec2(0.5, 0.5)
        rect_pos = _convert_coordinates(pivot, new_pivot, position, width, height)
        self.position = rect_pos


class Image(Control):
    texture: Texture2D | SubTexture2D | None

    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.texture = None
        self.color = Colors.White.copy()
        self.origin = vec2(0.5, 0.5)
        self.hfill_amount = 1.0
        self.vfill_amount = 1.0

    def rect(self) -> rl.Rectangle:
        if self.texture is None:
            return rl.Rectangle(0, 0, 0, 0)

        trans = self.transform()
        pos = trans._t()
        scale = trans._s()
        dest_width = self.texture.width * scale.x
        dest_height = self.texture.height * scale.y

        return rl.Rectangle(
            pos.x - dest_width * self.origin.x,
            pos.y - dest_height * self.origin.y,
            dest_width * self.hfill_amount,
            dest_height * self.vfill_amount,
        )
    
    def on_render_ui(self):
        if self.texture is None:
            return
        if type(self.texture) is Texture2D:
            main_tex = self.texture
            src_rect = rl.Rectangle(
                0, 0,
                main_tex.width * self.hfill_amount,
                main_tex.height * self.vfill_amount,
            )
        elif type(self.texture) is SubTexture2D:
            main_tex = self.texture.main_tex
            src_rect = rl.Rectangle(
                self.texture.src_x, self.texture.src_y,
                self.texture.width * self.hfill_amount,
                self.texture.height * self.vfill_amount,
            )
        else:
            raise TypeError(f"Unsupported texture type: {type(self.texture)}")
        rl.DrawTexturePro(main_tex, src_rect, self.rect(), vec2(0, 0), 0, self.color)

class TextBase(Control):
    font: rl.Font
    text: str

    @property
    def alpha(self) -> float:
        return self.color.a / 255
    
    @alpha.setter
    def alpha(self, value: float):
        self.color.a = int(value * 255)

    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.font = _g.default_font
        self.text = ""
        self.spacing = _g.default_text_spacing
        self.line_spacing = _g.default_text_line_spacing
        self.font_size = _g.default_font_size
        self.color = Colors.White.copy()

class Text(TextBase):
    """A text box for rendering long text with word wrap."""

    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.max_width = None
        self.max_height = None

    def __f(self, render: bool):
        assert self.font is not None
        assert self.max_width is not None
        pos = self.global_position
        rect = rl.Rectangle(
            pos.x,
            pos.y,
            self.max_width,
            self.max_height or 0.0,
        )
        limit_height = self.max_height is not None
        size = _rlDrawTextBoxed(render, limit_height, self.line_spacing, self.font, self.text, rect, self.font_size, self.spacing, True, self.color)
        return rl.Rectangle(pos.x, pos.y, size.x, size.y)

    def rect(self) -> rl.Rectangle:
        if self.font is None:
            return rl.Rectangle(0, 0, 0, 0)
        return self.__f(False)
    
    def on_render_ui(self):
        if self.font is None:
            return
        self.__f(True)


class Label(TextBase):
    """A simple label without word wrap."""
    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.origin = vec2(0.5, 0.5)

    def rect(self) -> rl.Rectangle:
        if self.font is None:
            return rl.Rectangle(0, 0, 0, 0)
        rl.SetTextLineSpacing(self.line_spacing + self.font_size)
        size = rl.MeasureTextEx(self.font, self.text, self.font_size, self.spacing)
        pos = self.global_position
        return rl.Rectangle(
            pos.x - size.x * self.origin.x,
            pos.y - size.y * self.origin.y,
            size.x,
            size.y,
        )

    def on_render_ui(self):
        if self.font is None:
            return
        draw_text(
            self.font,
            self.global_position,
            self.text,
            self.font_size,
            self.color,
            self.spacing,
            self.line_spacing,
            self.origin,
        )


class SpriteText(Control):
    font: SpriteFont
    text: str

    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.font = None
        self.text = ""
        self.spacing = 0
        self.color = Colors.White

    def on_render_ui(self):
        if self.font is None:
            return
        self.font.draw(self.transform(), self.text, self.spacing, self.color)

class Container(Control):
    width: float
    height: float
    origin: vec2
    color: rl.Color | None

    def __init__(self, name=None, parent=None) -> None:
        super().__init__(name, parent)
        self.width = _g.viewport_width
        self.height = _g.viewport_height
        self.origin = vec2(0.5, 0.5)
        self.color = None

    def rect(self) -> rl.Rectangle:
        trans = self.transform()
        pos = trans._t()
        scale = trans._s()
        dest_width = self.width * scale.x
        dest_height = self.height * scale.y
        return rl.Rectangle(
            pos.x - dest_width * self.origin.x,
            pos.y - dest_height * self.origin.y,
            dest_width,
            dest_height,
        )

    def create_inner_container(self, padding: vec2, name=None) -> 'Container':
        inner = Container(name=name, parent=self)
        inner.width = self.width - padding.x * 2
        inner.height = self.height - padding.y * 2
        inner.set_position(vec2(0, 0), vec2(0.5, 0.5), self.origin)
        return inner

    def on_render_ui(self):
        if self.color is not None:
            draw_rect(self.rect(), self.color, vec2(0, 0))
