import sys
import box2d
from linalg import *
import raylib as rl

import imgui

from _carrotlib import fast_apply, GRAPHICS_API_OPENGL_33, GRAPHICS_API_OPENGL_ES2, GRAPHICS_API_OPENGL_ES3, _request_hot_reload

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

class Game:
    instance: 'Game' = None

    def __init__(self):
        assert Game.instance is None
        Game.instance = self

    @property
    def design_size(self) -> tuple[int, int]:
        raise NotImplementedError
    
    @property
    def window_size(self) -> tuple[int, int]:
        return self.design_size
    
    @property
    def title(self):
        return "Game"

    def on_ready(self):
        if not rl.IsWindowReady():
            rl.InitWindow(self.window_size[0], self.window_size[1], self.title)
            rl.InitAudioDevice()
            imgui.rlImGuiSetup(True)
            imgui.GetIO().IniFilename = None    # disable imgui.ini

        # determine viewport scale
        design_size = self.design_size
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
        print('sys.platform:', sys.platform)
        print('viewport_size:', g.viewport_width, g.viewport_height)
        print('viewport_scale:', g.viewport_scale)
        print('screen_size:', rl.GetScreenWidth(), rl.GetScreenHeight())
        print('render_size:', rl.GetRenderWidth(), rl.GetRenderHeight())
        print('window_scale_dpi:', rl.GetWindowScaleDPI())
        print('GRAPHICS_API_OPENGL_33:', GRAPHICS_API_OPENGL_33)
        print('GRAPHICS_API_OPENGL_ES2:', GRAPHICS_API_OPENGL_ES2)
        print('GRAPHICS_API_OPENGL_ES3:', GRAPHICS_API_OPENGL_ES3)

        #############################################
        # temporary variables
        self.all_nodes = []
        self.all_nodes__append = self.all_nodes.append
        self.node_sort_key = lambda n: n.total_z_index()
        self.interactable_controls = []

        self.PIXEL_UNIT_TRANSFORM = mat3x3.trs(
                    vec2(g.viewport_width/2, g.viewport_height/2),
                    0,
                    vec2(g.PIXEL_PER_UNIT, g.PIXEL_PER_UNIT),
                )
        #############################################
        g.rl_camera_2d = rl.Camera2D(vec2(0,0), vec2(0,0), 0, g.viewport_scale)
        g.root = Node('root')
        g.b2_world = box2d.World()
        g.b2_world.set_debug_draw(DebugDraw())
        g.debug_window = DebugWindow()
        g.default_font = rl.GetFontDefault()
        g.default_font_size = 20
        g.default_material = UnlitMaterial()
        g.root.start_coroutine(_update_managed_sounds_coro())

    def on_update(self):
        all_nodes: list[Node] = self.all_nodes
        all_nodes__append = self.all_nodes__append
        node_sort_key = self.node_sort_key
        interactable_controls: list[Control] = self.interactable_controls

        all_nodes.clear()
        g.root.apply(all_nodes__append)
        fast_apply(Node._ready, all_nodes)

        # 1. physics update
        g.b2_world.step(rl.GetFrameTime(), 6, 2)

        # 2. input events
        all_nodes.clear()
        g.root.apply_enabled(all_nodes__append)

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
        self.PIXEL_UNIT_TRANSFORM.matmul(g.world_to_camera, out=g.world_to_viewport)

        if g.default_lightmap:
            g.default_lightmap.update()

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

        # hot reload feature
        if rl.IsKeyPressed(rl.KEY_F5):
            self._unload_resources()
            _request_hot_reload()

    def _unload_resources(self):
        _unload_all_sound_aliases()
        _unload_all_resources()
        for child in g.root.children.values():
            child.destroy()
        if g.default_lightmap:
            g.default_lightmap.destroy()

    def on_destroy(self):
        self._unload_resources()
        imgui.rlImGuiShutdown()
        rl.CloseAudioDevice()
        rl.CloseWindow()
