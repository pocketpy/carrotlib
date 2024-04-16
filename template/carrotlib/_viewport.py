import raylib as rl
from linalg import vec2, mat3x3

from . import g as _g

def get_mouse_position() -> vec2:
    """Get mouse position in viewport space."""
    return rl.GetMousePosition() / _g.viewport_scale

def get_mouse_delta() -> vec2:
    """Get mouse delta in viewport space."""
    return rl.GetMouseDelta() / _g.viewport_scale

def set_camera_transform(transform: mat3x3):
    """Set the camera transform.
    In order to make a node as camera, you need to call this function with the node's transform inside `on_update` method.

    Example:

    ```python
    class YourCamera(cl.Node):
        def on_update(self):
            cl.set_camera_transform(self.transform())
    """
    _g.world_to_camera.copy_(~transform)