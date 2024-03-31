import carrotlib as cl
import raylib as rl
from linalg import vec2

from timestone.actors.hero import Hero
from timestone.common.camera import Camera
from timestone import g

class DemoGround(cl.Node):
    def on_ready(self):
        self.tags.append(g.Tags.PLATFORM)

        self.b2_body = self.create_body()
        self.b2_body.set_box_shape(100, 1)
        self.b2_body.type = 0   # static
        self.b2_body.position = self.position = vec2(0, 5)

    def on_render(self):
        global_pos = self.global_position
        cl.draw_rect(rl.Rectangle(global_pos.x, global_pos.y, 200, 2), cl.Colors.Gray)


class ParallaxLayer(cl.Node):
    def __init__(self, camera: cl.Node, name=None, parent=None):
        super().__init__(name=name, parent=parent)
        self.camera = camera
        self.motion_scale = vec2(0, 0)
        self.prev_camera_position = vec2(0, 0)

    def on_ready(self):
        self.prev_camera_position.copy_(self.camera.global_position)

    def on_update(self):
        delta = self.camera.global_position - self.prev_camera_position
        delta.x *= self.motion_scale.x
        delta.y *= self.motion_scale.y
        self.global_position += delta
        self.prev_camera_position.copy_(self.camera.global_position)
        

class DemoLevel(cl.Node):
    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)

        self.camera = Camera()
        self.parallax = ParallaxLayer(self.camera, name='parallax')
        self.parallax.motion_scale = vec2(1, 1) * 0.5
        self.parallax.z_index = -1
        self.background = cl.nodes.Sprite(name='background', parent=self.parallax)
        self.background.texture = cl.load_texture_scaled('assets/demo_background.png', 0.5)

        self.ground = DemoGround(parent=self)
        self.ground.position = vec2(0, 10)

        # no parent, will be added to root
        Hero()
        

