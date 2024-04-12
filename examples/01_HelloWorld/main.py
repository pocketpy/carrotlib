import carrotlib as cl
import sys

class MyGame(cl.Game):
    def on_ready(self):
        super().on_ready()

        label = cl.controls.Label()
        label.text = "Hello, world"
        label.font_size = 100
        label.color = cl.Colors.Black
        
        label.position.x = cl.g.viewport_width / 2
        label.position.y = cl.g.viewport_height / 2

    @property
    def design_size(self):
        if sys.platform in ('ios', 'android'):
            return (0, 720)
        return (1280, 720)

