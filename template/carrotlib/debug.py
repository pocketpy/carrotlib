from linalg import vec2, vec4
import traceback
import raylib as rl
import c
import sys

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
            imgui.PushTextWrapPos()
            if type == 'stdout':
                imgui.TextColored(vec4(0.5, 1, 0.5, 1), msg)
            elif type == 'stderr':
                imgui.TextColored(vec4(1, 0.5, 0.5, 1), msg)
            else:
                imgui.Text(f'>>> {msg}')
            imgui.PopTextWrapPos()

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
    _selected: Node

    def __init__(self):
        self._selected = None

        self.variables = {}
        self.python_console = PythonConsole()

        # set window size
        self.w = rl.GetScreenWidth() * 0.35
        self.h = rl.GetScreenHeight() * 0.6

    @property
    def selected(self):
        if self._selected and self._selected._state != 1:
            self._selected = None
        return self._selected
    
    @selected.setter
    def selected(self, value):
        self._selected = value

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
        if not root.enabled:
            color = vec4(0.5, 0.5, 0.5, 1)
        elif isinstance(root, Control) and root.interactable:
            color = vec4(0, 1, 0, 1)
        else:
            color = vec4(1, 1, 1, 1)
        imgui.PushStyleColor(imgui.ImGuiCol_Text, color)
        expand = imgui.TreeNode(title, flags)
        imgui.PopStyleColor()

        if imgui.IsItemClicked(0):
            self.selected = root
            if imgui.IsMouseDoubleClicked(0):
                root.enabled = not root.enabled

        if root.enabled and len(root._coroutines) > 0:
            self.render_tree_colored_tag(f"({len(root._coroutines)})", vec4(1, 0.5, 0, 1))

        if root.tags:
            self.render_tree_colored_tag(f"[{','.join(root.tags)}]", vec4(0.1, 0.6, 1, 1))

        if expand:
            for child in root.children.values():
                self.render_hierarchy(child, depth+1)
            imgui.TreePop()

    def render_inspector(self, root, name=None, depth=0):
        """Render everything about the selected node with tree view"""
        root_d = root.__dict__
        is_container = isinstance(root, (list, dict, set)) or root_d
        flags = imgui.ImGuiTreeNodeFlags_SpanFullWidth
        if depth == 0:
            flags |= imgui.ImGuiTreeNodeFlags_DefaultOpen
        if not is_container:
            flags |= imgui.ImGuiTreeNodeFlags_Leaf

        if isinstance(root, (list, dict, set)):
            title = root.__class__.__name__ + f" (len={len(root)})"
        else:
            title = repr(root)

        if len(title) > 100:
            title = title[:100] + '...'

        if name is not None:
            # title = f"{name}: {title}"
            imgui.PushStyleColor(imgui.ImGuiCol_Text, vec4(0, 1, 0, 1))
            expand = imgui.TreeNode(name, flags)
            imgui.PopStyleColor()
            imgui.SameLine()
            imgui.Text(": " + title)
        else:
            expand = imgui.TreeNode(title, flags)

        if expand:
            if isinstance(root, list):
                for i in range(len(root)):
                    self.render_inspector(root[i], f"[{i}]", depth+1)
            elif isinstance(root, dict):
                for k, v in root.items():
                    self.render_inspector(v, repr(k), depth+1)
            elif root_d:
                for name in sorted(root_d.keys()):
                    if name.startswith('_'):
                        continue
                    self.render_inspector(root_d[name], name, depth+1)
            imgui.TreePop()

    def render(self):
        imgui.SetNextWindowSize(vec2(self.w, self.h), imgui.ImGuiCond_FirstUseEver)
        imgui.SetNextWindowPos(vec2(0, 0), imgui.ImGuiCond_FirstUseEver)
        imgui.SetNextWindowCollapsed(True, imgui.ImGuiCond_FirstUseEver)
        imgui.Begin("Debug Window")

        imgui.BeginTabBar("DebugTabBar")
        if imgui.BeginTabItem("Hierarchy"):
            imgui.BeginChild("Hierarchy", vec2(0, self.h * 0.6), False, 0)
            self.render_hierarchy(g.root)
            imgui.EndChild()

            imgui.Separator()

            imgui.BeginChild("Properties", vec2(0, 0), False, 0)
            if self.selected:
                for line in self.selected.__debuginfo__():
                    imgui.PushTextWrapPos()
                    imgui.Text(line)
                    imgui.PopTextWrapPos()
            else:
                imgui.Text("Nothing selected")
            imgui.EndChild()
            imgui.EndTabItem()

        if imgui.BeginTabItem("Variables"):
            imgui.BeginChild("Variables", vec2(0, 0), False, 0)
            for name, value in self.variables.items():
                value_repr = repr(value)
                value_repr = '\n' + value_repr if '\n' in value_repr else value_repr
                imgui.Text(f"{name}: {value_repr}")
                imgui.Separator()

            imgui.EndChild()
            imgui.EndTabItem()

        if imgui.BeginTabItem("Console"):
            self.python_console.render()
            imgui.EndTabItem()

        if imgui.BeginTabItem("Inspector"):
            if self.selected is None:
                imgui.Text("Nothing selected")
            else:
                self.render_inspector(self.selected)
            imgui.EndTabItem()

        imgui.EndTabBar()
        imgui.End()
