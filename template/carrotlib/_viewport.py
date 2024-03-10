import raylib as rl
from linalg import vec2, mat3x3

from . import g as _g

def get_mouse_position() -> vec2:
    """Get mouse position in viewport space"""
    return rl.GetMousePosition() / _g.viewport_scale

def get_mouse_delta() -> vec2:
    """Get mouse delta in viewport space"""
    return rl.GetMouseDelta() / _g.viewport_scale

def set_camera_transform(transform: mat3x3):
    _g.world_to_camera.copy_(~transform)