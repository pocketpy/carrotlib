from linalg import *
import raylib as rl
import box2d
from _carrotlib import fast_apply
from . import g as _g

class Node:
    on_ready = lambda self: None
    on_update = lambda self: None
    on_render = lambda self: None
    on_render_ui = lambda self: None
    on_destroy = lambda self: None

    parent: 'Node'
    children: dict[str, 'Node']

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name=None, parent=None) -> None:
        # private fields
        self._name = name or hex(id(self))
        self._coroutines = []           # running coroutines
        self._alive_coroutines = []     # alive coroutines
        self._state = 0                 # unready -> ready -> destroyed
        self._raii_objects = []         # objects that will be destroyed when this node is destroyed
        # transform
        self.position = vec2(0, 0)
        self.rotation = 0           # in radians
        self.scale = vec2(1, 1)
        # hierarchy
        self.children = {}
        # settings
        self.z_index = 0
        self.enabled = True

        if parent is None:
            parent = _g.root
        self.parent = parent

        if parent is not None:
            if self._name in parent.children:
                raise ValueError(f'duplicated child name {self._name!r}')
            parent.children[self._name] = self

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
        return f'<{cls_name} {self.path}>'
    
    @property
    def path(self) -> str:
        if self.parent is None:
            return ''   # omit `root`
        return self.parent.path + '/' + self.name
    
    def total_z_index(self) -> int:
        if self.parent is None:
            return self.z_index
        return self.parent.total_z_index() + self.z_index

    def get_node(self, path: str) -> 'Node':
        """get the child node by path"""
        names = path.split('/')
        node = self
        for name in names:
            node = node.children[name]
        return node
    
    def create_body(self) -> box2d.Body:
        """create a box2d body attached to this node with RAII enabled"""
        return self.RAII(box2d.Body(_g.b2_world, node=self))
    
    def RAII(self, obj):
        """automatically destroy the object when this node is destroyed
        
        + `obj`: an object which contains a `destroy` method
        """
        self._raii_objects.append(obj)
        return obj
    
    def transform(self) -> mat3x3:
        """get the transform matrix from world space to local space"""
        if self.parent is None:
            return mat3x3.identity()
        t = self.parent.transform()
        t.__imatmul__(mat3x3.trs(self.position, self.rotation, self.scale))
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
                obj = next(coroutine)
                if obj is not StopIteration:
                    self._alive_coroutines.append(coroutine)
            self._coroutines, self._alive_coroutines = self._alive_coroutines, self._coroutines
            self._alive_coroutines.clear()

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
        self._raii_objects.clear()

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

    def on_box2d_pre_step(self):
        pass

    def on_box2d_post_step(self):
        pass



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