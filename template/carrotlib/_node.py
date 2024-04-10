from linalg import *
import raylib as rl
import box2d
import math
from typing import Literal

from _carrotlib import fast_apply
from . import g as _g

class Node:
    def on_ready(self): pass
    def on_update(self): pass
    def on_render(self): pass
    def on_render_ui(self): pass
    def on_destroy(self): pass
    def on_box2d_pre_step(self): pass
    def on_box2d_post_step(self): pass

    parent: 'Node'
    children: dict[str, 'Node']

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name=None, parent=None) -> None:
        # private fields
        self._name = name or hex(id(self))
        self._coroutines = []           # running coroutines
        self._living_coroutines = []    # living coroutines
        self._state = 0                 # unready -> ready -> destroyed
        self._cached_transform = mat3x3.identity()
        self._raii_objects = []
        # transform
        self.position = vec2(0, 0)
        self.rotation = 0           # in radians
        self.scale = vec2(1, 1)
        # hierarchy
        self.children = {}
        # settings
        self.z_index = 0
        self.enabled = True
        self.tags = []

        self.parent = parent or _g.root
        if self.parent is not None:
            if self._name in self.parent.children:
                raise ValueError(f'duplicated child name {self._name!r}')
            self.parent.children[self._name] = self

    @property
    def state(self) -> Literal[0, 1, 2]:
        return self._state

    @property
    def global_position(self) -> vec2:
        return self.transform()._t()
    
    @global_position.setter
    def global_position(self, value: vec2):
        t = self.parent.transform()
        t.invert_()
        self.position = t.transform_point(value)

    def __repr__(self):
        cls_name = type(self).__name__
        if self._state == 2:
            return f'<{cls_name} (destroyed)>'
        return f'<{cls_name} {self.path}>'
    
    def __debuginfo__(self):
        degree = math.degrees(self.rotation)
        return [
            f"position: {self.position}",
            f"rotation: {self.rotation:.2f} ({degree:.1f}°)",
            f"scale: {self.scale}",
            f"total_z_index: {self.total_z_index()}",
        ]
    
    @property
    def path(self) -> str:
        cpnts = []
        node = self
        while node is not _g.root:
            cpnts.append(node.name)
            node = node.parent
        cpnts.reverse()
        return '/'.join(cpnts)
    
    def total_z_index(self) -> int | float:
        res = self.z_index
        node = self
        while node.parent is not None:
            node = node.parent
            res += node.z_index
        return res

    def get_node(self, path: str) -> 'Node':
        """get the child node by path"""
        node = self
        for name in path.split('/'):
            node = node.children[name]
        return node
    
    def create_body(self, with_callback=True) -> box2d.Body:
        """create a box2d body attached to this node"""
        b2_body = box2d.Body(_g.b2_world, node=self, with_callback=with_callback)
        self._raii_objects.append(b2_body)
        return b2_body
    
    def transform(self) -> mat3x3:
        """get the transform matrix from world space to local space"""
        if self.parent is None:
            return mat3x3.identity()
        t = self.parent.transform()
        self._cached_transform.copy_trs_(self.position, self.rotation, self.scale)
        t.matmul(self._cached_transform, out=t)
        return t

    def _ready(self):
        # call on_ready only once
        if self._state == 0:
            self.on_ready()
            self._state = 1

    def _update(self):
        if self._state != 1:
            return
        self.on_update()
        # update coroutines
        if self._coroutines:
            for coroutine in self._coroutines:
                # None means a coroutine was stopped by user
                # we cannot remove it immediately because it will break the loop
                if coroutine is None:
                    continue
                if next(coroutine) is not StopIteration:
                    self._living_coroutines.append(coroutine)
            self._coroutines, self._living_coroutines = self._living_coroutines, self._coroutines
            self._living_coroutines.clear()

    def _render(self):
        if self._state == 1:
            self.on_render()

    def _render_ui(self):
        if self._state == 1:
            self.on_render_ui()

    def _destroy(self):
        if self._state == 2:
            return
        self._state = 2
        self.on_destroy()
        self.stop_all_coroutines()
        for obj in self._raii_objects:
            obj.destroy()

    def apply(self, f):
        f(self)
        fast_apply(Node.apply, self.children.values(), f)

    def apply_enabled(self, f):
        if not self.enabled:
            return
        f(self)
        fast_apply(Node.apply_enabled, self.children.values(), f)

    def is_ancestor_of(self, node: 'Node') -> bool:
        """check if this node is an ancestor of `node`"""
        while node is not None:
            if node is self:
                return True
            node = node.parent
        return False

    def destroy(self):
        if self._state == 2:
            return
        if self is _g.root:
            raise ValueError('cannot destroy root node')
        self.apply(Node._destroy)
        # print(self.parent.children.keys(), self.name, self.name in self.parent.children)
        del self.parent.children[self.name]
        self.parent = None

    def destroy_later(self, delay: float):
        _g.root.start_coroutine(_DestroyLater(delay, self))
    
    def start_coroutine(self, coroutine):
        self._coroutines.append(coroutine)
        return coroutine

    def stop_coroutine(self, coroutine):
        for i in range(len(self._coroutines)):
            if self._coroutines[i] is coroutine:
                self._coroutines[i] = None
                break

    def stop_all_coroutines(self):
        for i in range(len(self._coroutines)):
            self._coroutines[i] = None



def get_node(path: str) -> Node:
    return _g.root.get_node(path)


def build_scene_tree(tree: dict, locals: dict, root: Node = None):
    root: Node = root or _g.root
    for key, child in tree.items():
        if key == '_':
            for k, v in child.items():
                setattr(root, k, v)
            continue
        name, T = key.split('|')
        T = locals[T]
        node = T(name, parent=root)
        if child is not None:
            build_scene_tree(child, locals, node)

class WaitForSeconds:
    def __init__(self, seconds: float):
        self._seconds = seconds
        self._t = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        self._t += rl.GetFrameTime()
        if self._t >= self._seconds:
            return StopIteration
        return None
    
class WaitForEndOfFrame:
    def __iter__(self):
        return self
    
    def __next__(self):
        return StopIteration
    
class _DestroyLater(WaitForSeconds):
    def __init__(self, seconds: float, node: Node):
        super().__init__(seconds)
        self.node = node

    def __next__(self):
        obj = super().__next__()
        if obj is StopIteration:
            self.node.destroy()
            return obj