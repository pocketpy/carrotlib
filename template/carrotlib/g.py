from typing import TYPE_CHECKING

from linalg import mat3x3
import raylib as rl

if TYPE_CHECKING:
    from box2d import World
    from ._node import Node
    from .controls import Control
    from .debug import DebugWindow
    from ._light import Lightmap

root: Node = None
b2_world: World = None

debug_window: DebugWindow = None
debug_draw_box2d: bool = False

background: rl.Color = rl.Color(255, 255, 255, 255)

# updated by engine every frame
hovered_control: Control = None
pressed_control: Control = None

# how many pixels in one virtual unit, this makes box2d work
# box2d requires objects to be in the range of 0.1 ~ 10 units
# box2d requires world to be in the range of -1000 ~ 1000 units
PIXEL_PER_UNIT = 10

# world space to camera space matrix (set by user)
world_to_camera: mat3x3 = mat3x3.identity()
# world space to viewport space matrix (updated by engine every frame)
world_to_viewport: mat3x3 = mat3x3.identity()

is_rendering_ui: bool = False

viewport_width: int = None
viewport_height: int = None

viewport_scale: float = None

rl_camera_2d: rl.Camera2D = None

default_font: rl.Font = None
default_font_size: int = None

lightmap: Lightmap = None


class DefaultMaterial:
    def __enter__(self): pass
    def __exit__(self, *args): pass

default_material = DefaultMaterial()

