import carrotlib as cl
from linalg import vec2

class MyGame(cl.Game):
    def on_ready(self):
        super().on_ready()

        label = cl.controls.Label()
        label.text = "Hello, world"
        label.font_size = 100
        label.color = cl.Colors.Black
        label.position = vec2(640, 360)

    @property
    def design_size(self):
        return (1280, 720)
