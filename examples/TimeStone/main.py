import carrotlib as cl
import raylib as rl
from linalg import vec2

class Timestone(cl.Game):
    def on_ready(self):
        super().on_ready()
        cl.g.background = cl.Color(201, 174, 135, 255)
        cl.g.debug_draw_box2d = True
        cl.g.b2_world.gravity = vec2(0, 98)

        from timestone.levels import DemoLevel
        DemoLevel()

    @property
    def design_size(self):
        return (320, 180)
    
    @property
    def window_size(self):
        return (1280, 720)
    
    @property
    def title(self):
        return 'TimeStoneGame'
