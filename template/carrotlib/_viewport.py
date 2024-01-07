import raylib as rl
from linalg import vec2

from . import g as _g

def get_mouse_position() -> vec2:
    """Get mouse position in viewport space"""
    return rl.GetMousePosition() / _g.viewport_scale

def get_mouse_delta() -> vec2:
    """Get mouse delta in viewport space"""
    return rl.GetMouseDelta() / _g.viewport_scale

__all__ = [
    'get_mouse_position',
    'get_mouse_delta',
]