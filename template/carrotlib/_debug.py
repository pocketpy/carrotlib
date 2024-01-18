from linalg import vec2, vec4
import traceback
import math
import c

import imgui

from ._node import Node
from .controls import Control

from . import g

class PythonContext:
    def __init__(self, console: 'PythonConsole'):
        self.g = g
        self._console = console

    def print(self, obj):
        self._console.history.append(('stdout', str(obj)))


class PythonConsole:
    def __init__(self):
        self.history = []
        self.buffer = c.struct(1024)
        self.context = PythonContext(self)

    def get_buffer_str(self):
        p = self.buffer.addr()
        return c.p_cast(p, c.char_p).read_string()
    
    def render_history(self):
        for type, msg in self.history:
            if type == 'stdout':
                imgui.TextColored(vec4(0.5, 1, 0.5, 1), msg)
            elif type == 'stderr':
                imgui.TextColored(vec4(1, 0.5, 0.5, 1), msg)
            else:
                imgui.Text(f'>>> {msg}')

    def render(self):
        height = imgui.GetFrameHeight()
        imgui.BeginChild("##history", vec2(0, height-120), True)
        self.render_history()

        # auto scroll here
        if imgui.GetScrollY() >= imgui.GetScrollMaxY():
            imgui.SetScrollHereY(1.0)
        imgui.EndChild()

        # full width
        imgui.PushItemWidth(-1)
        ok = imgui.InputText(
            "##src",
            self.buffer.addr(), 
            self.buffer.sizeof(),
            imgui.ImGuiInputTextFlags_EnterReturnsTrue
        )
        if imgui.IsWindowFocused() and not imgui.IsAnyItemActive():
            imgui.SetKeyboardFocusHere(-1)

        imgui.Text("Enter: eval, Ctrl+Enter: exec")

        # enter for eval, ctrl+enter for exec
        if ok:
            src = self.get_buffer_str()
            self.history.append(('stdin', src))
            if src:
                if not imgui.GetIO().KeyCtrl:
                    try:
                        ret = eval(src, self.context.__dict__)
                        self.history.append(('stdout', repr(ret)))
                    except:
                        self.history.append(('stderr', traceback.format_exc()))
                else:
                    try:
                        exec(src, self.context.__dict__)
                    except:
                        self.history.append(('stderr', traceback.format_exc()))
            c.memset(self.buffer.addr(), 0, self.buffer.sizeof())

class DebugWindow:
    selected: Node

    def __init__(self):
        self.selected = None
        self.variables = {}
        self.python_console = PythonConsole()

    def render_tree_colored_tag(self, text: str, color: vec4):
        imgui.SameLine(0, 8)
        imgui.PushStyleColor(imgui.ImGuiCol_Text, color)
        imgui.Text(text)
        imgui.PopStyleColor()

    def render_hierarchy(self, root: Node, depth=0):
        flags = imgui.ImGuiTreeNodeFlags_OpenOnArrow \
            | imgui.ImGuiTreeNodeFlags_SpanFullWidth
        if depth <= 1:
            flags |= imgui.ImGuiTreeNodeFlags_DefaultOpen
        if root is self.selected:
            flags |= imgui.ImGuiTreeNodeFlags_Selected
        if not root.children:
            flags |= imgui.ImGuiTreeNodeFlags_Leaf

        title = root.name + f" <{type(root).__name__}>"

        # if not enabled use gray color
        DISABLED_COLOR = vec4(0.5, 0.5, 0.5, 1)
        if not root.enabled:
            imgui.PushStyleColor(imgui.ImGuiCol_Text, DISABLED_COLOR)
        expand = imgui.TreeNode(title, flags)

        if imgui.IsItemClicked(0):
            self.selected = root
        if imgui.IsItemClicked(0) and imgui.IsMouseDoubleClicked(0):
            self.selected = root
            root.enabled = not root.enabled

        if isinstance(root, Control) and root.interactable:
            color = vec4(0, 1, 0, 1) if root.enabled else DISABLED_COLOR
            self.render_tree_colored_tag('[ui]', color)

        if root.enabled and len(root._coroutines) > 0:
            self.render_tree_colored_tag(f"[{len(root._coroutines)}]", vec4(1, 0.5, 0, 1))

        if root.tags:
            self.render_tree_colored_tag(f"[{','.join(root.tags)}]", vec4(0.1, 0.6, 1, 1))

        if not root.enabled:
            imgui.PopStyleColor()

        if expand:
            for child in root.children.values():
                self.render_hierarchy(child, depth+1)
            imgui.TreePop()

    def render(self):
        # set window size
        imgui.SetNextWindowSize(vec2(500, 500), imgui.ImGuiCond_FirstUseEver)
        imgui.SetNextWindowCollapsed(True, imgui.ImGuiCond_FirstUseEver)
        imgui.Begin("Debug Window")

        imgui.BeginTabBar("DebugTabBar")
        if imgui.BeginTabItem("Hierarchy"):
            height = imgui.GetFrameHeight()
            imgui.BeginChild("Hierarchy", vec2(0, height-200), False, 0)
            self.render_hierarchy(g.root)
            imgui.EndChild()

            imgui.Separator()

            imgui.BeginChild("Properties", vec2(0, 0), False, 0)
            if self.selected:
                imgui.Text(f"position: {self.selected.position}")
                degree = math.degrees(self.selected.rotation)
                imgui.Text(f"rotation: {self.selected.rotation:.2f} ({degree:.2f}°)")
                imgui.Text(f"scale: {self.selected.scale}")
                imgui.Text(f"total_z_index: {self.selected.total_z_index()}")
                imgui.Text(f"tags: {self.selected.tags}")
            else:
                imgui.Text("Nothing selected")
            imgui.EndChild()
            imgui.EndTabItem()

        if imgui.BeginTabItem("Variables"):
            imgui.BeginChild("Variables", vec2(0, 0), False, 0)
            for name, value in self.variables.items():
                imgui.Text(f"{name}: {value!r}")
            imgui.EndChild()
            imgui.EndTabItem()

        if imgui.BeginTabItem("Console"):
            self.python_console.render()
            imgui.EndTabItem()

        imgui.EndTabBar()
        imgui.End()
