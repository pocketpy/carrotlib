from linalg import vec2
import carrotlib as cl
import raylib as rl
import math
import box2d
from timestone import g

def get_horizontal_movement() -> float:
    value = 0
    # keyboard
    if rl.IsKeyDown(rl.KEY_A) or rl.IsKeyDown(rl.KEY_LEFT):
        value -= 1.0
    if rl.IsKeyDown(rl.KEY_D) or rl.IsKeyDown(rl.KEY_RIGHT):
        value += 1.0
    # gamepad
    # value += rl.GetGamepadAxisMovement(0, rl.GAMEPAD_AXIS_LEFT_X)
    return value

def is_jump_button_pressed() -> bool:
    return rl.IsKeyPressed(rl.KEY_SPACE) or rl.IsKeyPressed(rl.KEY_W) or rl.IsKeyPressed(rl.KEY_UP)

class ArrowDestroyFX(cl.nodes.Sprite):
    def __init__(self, name=None):
        super().__init__(name=name, parent=None)
        self.animator = cl.FramedAnimator()
        self.animator['_'] = cl.load_framed_animation('assets/sprites/demo/arrow/destroy', 12)
        self.animator.play('_')

    def on_update(self):
        self.texture = self.animator.update()
        if self.texture is None:
            self.destroy()

class Arrow(cl.nodes.Sprite):
    def __init__(self, name=None):
        super().__init__(name=name, parent=None)
        self.texture = cl.load_texture('assets/sprites/demo/arrow/idle/1.png')
        self.b2_body = self.create_body()

        radius = self.texture.height / 2 / cl.g.PIXEL_PER_UNIT * 0.8
        self.b2_body.set_circle_shape(radius)
        self.b2_body.gravity_scale = 0.2
        self.b2_body.is_sensor = True
        self.b2_body.bullet = True
        self.origin = vec2(0.9, 0.5)
    
    def on_ready(self):
        self.b2_body.position = self.position
        self.b2_body.rotation = self.rotation

    def on_box2d_post_step(self):
        self.position = self.b2_body.position
        self.rotation = self.b2_body.rotation = vec2.angle(vec2(1, 0), self.b2_body.velocity)

    def on_box2d_contact_begin(self, other: box2d.Body):
        if g.Tags.PLATFORM in other.node.tags:
            self.destroy()
            fx = ArrowDestroyFX()
            fx.position = self.position
            return

class HeroBow(cl.nodes.Sprite):
    parent: 'Hero'
    def __init__(self, name=None, parent=None):
        super().__init__(name=name, parent=parent)
        self.normal_tex = cl.load_texture('assets/sprites/demo/bow_1.png')
        self.charge_tex = cl.load_texture('assets/sprites/demo/bow_2.png')
        self.origin.y = 0.52
        self.position.y = 0.7

    def on_update(self):
        self.flip_x = self.parent.body.flip_x
        if self.flip_x:
            flip_scale = -1
            self.origin.x = 1 - 0.28
            self.position.x = -0.8
        else:
            flip_scale = 1
            self.origin.x = 0.28
            self.position.x = 0.8

        direction = cl.get_mouse_position() - cl.g.world_to_viewport.transform_point(self.global_position)
        self.rotation = cl.clamp(
            vec2.angle(vec2(flip_scale, 0), direction),
            math.radians(-80 * flip_scale),
            math.radians(20 * flip_scale)
        )

        if rl.IsMouseButtonDown(0):
            self.texture = self.charge_tex
        else:
            self.texture = self.normal_tex

        if rl.IsMouseButtonReleased(0):
            arrow = Arrow()
            arrow.position = self.global_position
            arrow.rotation = self.rotation
            arrow.b2_body.velocity = vec2(24 * flip_scale, 0).rotate(self.rotation)

class Hero(cl.Node):
    def __init__(self, name=None):
        super().__init__(name=name, parent=None)

        g.hero = self

        self.b2_body = self.create_body()
        self.b2_body.set_box_shape(1.6/2, 3.0/2)
        self.b2_body.fixed_rotation = True
        self.b2_body.position = self.position = vec2(0, 0)

        self.speed = 10
        self.jump_speed = -30

        self.body = cl.nodes.Sprite(name='body', parent=self)
        self.body_animator = cl.FramedAnimator()
        self.body_animator['idle'] = cl.load_framed_animation('assets/sprites/hero/idle', 12, 'forward')
        self.body_animator['walk'] = cl.load_framed_animation('assets/sprites/hero/walk', 12, 'forward')

        self.bow = HeroBow(name='bow', parent=self)

    def on_box2d_post_step(self):
        self.position.copy_(self.b2_body.position)

    def is_on_platform(self) -> bool:
        if not math.isclose(self.b2_body.velocity.y, 0):
            return False
        contacts = self.b2_body.get_contacts()
        for contact in contacts:
            if g.Tags.PLATFORM in contact.node.tags:
                return True
        return False

    def on_update(self):
        velocity = self.b2_body.velocity
        velocity.x = get_horizontal_movement() * self.speed
        is_on_platform = self.is_on_platform()
        if is_jump_button_pressed() and is_on_platform:
            velocity.y = self.jump_speed
        self.b2_body.velocity = velocity

        # update body animations
        if is_on_platform:
            if math.isclose(velocity.x, 0):
                self.body_animator.play('idle')
            else:
                self.body_animator.play('walk')
                self.body.flip_x = velocity.x < 0
        else:
            self.body_animator.play('idle')
            if not math.isclose(velocity.x, 0):
                self.body.flip_x = velocity.x < 0

        self.body.texture = self.body_animator.update()
        

