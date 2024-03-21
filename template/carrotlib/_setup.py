import sys
import box2d
from linalg import *
import raylib as rl

import imgui

from _carrotlib import fast_apply

from . import g
from ._node import Node
from .controls import Control
from ._renderer import DebugDraw
from ._sound import _unload_all_sound_aliases, _update_managed_sounds_coro, _count_managed_sounds
from ._resources import _unload_all_resources
from .debug import DebugWindow
from ._viewport import get_mouse_position
from ._material import UnlitMaterial

class RestartException(Exception):
    pass

_should_restart_app = False

class Callbacks:
    def on_ready(self):
        g.rl_camera_2d = rl.Camera2D(vec2(0,0), vec2(0,0), 0, g.viewport_scale)
        g.root = Node('root')
        g.b2_world = box2d.World()
        g.b2_world.set_debug_draw(DebugDraw())
        g.debug_window = DebugWindow()
        g.default_material = UnlitMaterial()
        g.root.start_coroutine(_update_managed_sounds_coro())

    def on_pre_render(self):
        if g.default_lightmap:
            g.default_lightmap.update()

    def on_destroy(self):
        _unload_all_sound_aliases()
        _unload_all_resources()
        for child in g.root.children.values():
            child.destroy()
        if g.default_lightmap:
            g.default_lightmap.destroy()


def main(callbacks: Callbacks, design_size: tuple[int, int]=None, window_size: tuple[int, int]=None, title="Game"):
    global _should_restart_app

    assert design_size is not None

    if window_size is None:
        window_size = design_size

    rl.SetTraceLogLevel(rl.LOG_WARNING)

    if not rl.IsWindowReady():
        rl.InitWindow(window_size[0], window_size[1], title)
        rl.InitAudioDevice()
        imgui.rlImGuiSetup(True)
        imgui.GetIO().IniFilename = None    # disable imgui.ini

    # determine viewport scale
    g.viewport_width, g.viewport_height = design_size
    assert type(design_size[0]) is int and type(design_size[1]) is int

    if g.viewport_height == 0:
        assert g.viewport_width != 0
        g.viewport_scale = rl.GetScreenWidth() / g.viewport_width
        g.viewport_height = int(rl.GetScreenHeight() / g.viewport_scale)
    elif g.viewport_width == 0:
        assert g.viewport_height != 0
        g.viewport_scale = rl.GetScreenHeight() / g.viewport_height
        g.viewport_width = int(rl.GetScreenWidth() / g.viewport_scale)
    else:
        g.viewport_scale = rl.GetScreenHeight() / g.viewport_height

    print('sys.version:', sys.version)
    print('viewport_size:', g.viewport_width, g.viewport_height)
    print('viewport_scale:', g.viewport_scale)
    print('screen_size:', rl.GetScreenWidth(), rl.GetScreenHeight())
    print('render_size:', rl.GetRenderWidth(), rl.GetRenderHeight())
    print('window_scale_dpi:', rl.GetWindowScaleDPI())

    # intialization
    callbacks.on_ready()

    # temporary variables
    all_nodes: list[Node] = []
    all_nodes__append = all_nodes.append
    node_sort_key = lambda n: n.total_z_index()
    interactable_controls: list[Control] = []

    PIXEL_UNIT_TRANSFORM = mat3x3.trs(
                vec2(g.viewport_width/2, g.viewport_height/2),
                0,
                vec2(g.PIXEL_PER_UNIT, g.PIXEL_PER_UNIT),
            )

    while not rl.WindowShouldClose():
        if _should_restart_app:
            _should_restart_app = False
            callbacks.on_destroy()
            raise RestartException

        all_nodes.clear()
        g.root.apply(all_nodes__append)
        fast_apply(Node._ready, all_nodes)

        # 1. physics update
        g.b2_world.step(rl.GetFrameTime(), 6, 2)

        # 2. input events
        all_nodes.clear()
        g.root.apply_enabled(all_nodes__append)

        # hot reload feature
        if rl.IsKeyPressed(rl.KEY_F5):
            _should_restart_app = True

        interactable_controls.clear()
        g.hovered_control = None

        for node in all_nodes:
            if isinstance(node, Control) and node.interactable and node._state == 1:
                interactable_controls.append(node)
        # make the most recently rendered control on top
        interactable_controls.reverse()
        for c in interactable_controls:
            if rl.CheckCollisionPointRec(get_mouse_position(), c.rect()):
                g.hovered_control = c
                break

        # 3. update
        fast_apply(Node._update, all_nodes)

        # 4. render
        # update world_to_viewport
        PIXEL_UNIT_TRANSFORM.matmul(g.world_to_camera, out=g.world_to_viewport)

        callbacks.on_pre_render()

        rl.BeginDrawing()
        rl.BeginMode2D(g.rl_camera_2d)
        rl.ClearBackground(g.background)

        # NOTE: after updates, the nodes may be changed (enabled/disabled)
        all_nodes.clear()
        g.root.apply_enabled(all_nodes__append)

        # render scene (sort by z-index via stable sort)
        all_nodes.sort(key=node_sort_key)
        fast_apply(Node._render, all_nodes)

        # render gizmos
        # enum
        # {
        # 	e_shapeBit				= 0x0001,	///< draw shapes
        # 	e_jointBit				= 0x0002,	///< draw joint connections
        # 	e_aabbBit				= 0x0004,	///< draw axis aligned bounding boxes
        # 	e_pairBit				= 0x0008,	///< draw broad-phase pairs
        # 	e_centerOfMassBit		= 0x0010	///< draw center of mass frame
        # };
        if g.debug_draw_box2d:
            g.b2_world.debug_draw(0x0001 | 0x0002 | 0x0008 | 0x0010)

        # 5. render ui
        g.is_rendering_ui = True
        fast_apply(Node._render_ui, all_nodes)
        g.is_rendering_ui = False
        rl.EndMode2D()

        # right top
        rl.DrawFPS(rl.GetScreenWidth()-100, 0)

        # 6. submit
        imgui.NewFrame()
        g.debug_window.variables['mouse_pos'] = get_mouse_position()
        g.debug_window.variables['gesture'] = rl.Gesture_NAMES[rl.GetGestureDetected()]
        g.debug_window.variables['hovered_control'] = g.hovered_control
        g.debug_window.variables['managed_sounds'] = _count_managed_sounds()
        g.debug_window.variables['world_to_viewport'] = g.world_to_viewport
        g.debug_window.render()
        imgui.Render()
        rl.EndDrawing()

    callbacks.on_destroy()

    imgui.rlImGuiShutdown()
    rl.CloseAudioDevice()
    rl.CloseWindow()

