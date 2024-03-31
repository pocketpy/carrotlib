import carrotlib as cl
import raylib as rl
from linalg import vec2

from timestone import g

class Camera(cl.Node):
    def __init__(self, name='camera', parent=None) -> None:
        super().__init__(name, parent)

        self.current_velocity = vec2(0, 0)

    def on_update(self):
        if g.hero is None:
            return
        target: vec2 = g.hero.global_position + vec2(0, -2)
        curr_pos = self.global_position
        smooth_time = 0.2
        next_pos = vec2.smooth_damp(curr_pos, target, self.current_velocity, smooth_time, 100, rl.GetFrameTime())
        self.global_position = next_pos
        cl.set_camera_transform(self.transform())
