
import carrotlib as cl

class MyGame(cl.Game):
    def on_ready(self):
        super().on_ready()
        # TODO: 初始化你的游戏

    @property
    def design_size(self):
        return (1280, 720)
