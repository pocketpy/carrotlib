import box2d
from collections import defaultdict
from linalg import *
import raylib as rl

from ..ldtk.layer import AutoTiledLayer

from .._node import Node
from .._colors import Colors

from .. import g as _g

class _Vertex:
    def __init__(self, x: int, y: int, neighbors: list, count: int):
        self.x = x
        self.y = y
        self.neighbors = neighbors
        self.count = count

    def __repr__(self):
        return f'({self.x}, {self.y})'

class _Edge:
    def __init__(self):
        self.count = 0
        self.cell_pos = None

def simplify(path: list[_Vertex]):
    simplied = [path[0]]
    for i in range(1, len(path) - 1):
        prev = path[i - 1]
        curr = path[i]
        next = path[i + 1]
        if prev.x == curr.x == next.x or prev.y == curr.y == next.y:
            continue
        else:
            simplied.append(curr)
    # check the last vertex
    prev = simplied[-1]
    curr = path[-1]
    next = simplied[0]
    if prev.x == curr.x == next.x or prev.y == curr.y == next.y:
        pass
    else:
        simplied.append(path[-1])
    return simplied

class _TilemapColliderSolver:
    map: 'Tilemap'
    vertices: dict[tuple[int, int], _Vertex]
    edges: dict[tuple[int, int, int, int], _Edge]

    def __init__(self, map: 'Tilemap'):
        self.map = map
        self.vertices = {}
        self.edges = defaultdict(_Edge)
        for y in range(map.height):
            for x in range(map.width):
                if not map.has_cell(x, y):
                    continue
                # put edges into `self.edges`
                self.add_edge(x, y, x+1, y, (x, y))
                self.add_edge(x, y, x, y+1, (x, y))
                self.add_edge(x+1, y, x+1, y+1, (x, y))
                self.add_edge(x, y+1, x+1, y+1, (x, y))
        # keeps only edges with 1 count
        self.edges = {k: v for k, v in self.edges.items() if v.count == 1}
        # put vertices into `self.vertices`
        for x, y, z, w in self.edges.keys():
            self.vertices[(x, y)] = None
            self.vertices[(z, w)] = None
        # process vertices
        for x, y in self.vertices.keys():
            neighbors = [
                z
                for z in [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
                if (x, y, z[0], z[1]) in self.edges
            ]
            assert len(neighbors) in (2, 4)
            if len(neighbors) == 4:
                count = 2       # self-intersecting vertex
            else:
                count = 1       # trivial vertex
            v = _Vertex(x, y, neighbors, count)
            self.vertices[(x, y)] = v

    # TODO: 处理对角、非连通、内嵌情况
    def dfs(self, curr: _Vertex, path: list[_Vertex]):
        assert curr.count > 0
        curr.count -= 1
        if len(path) == 0:
            prev = None
        else:
            prev = path[-1]
        path.append(curr)
        if len(curr.neighbors) == 2:
            n0 = self.vertices[curr.neighbors[0]]
            n1 = self.vertices[curr.neighbors[1]]
            if n0.count > 0 and n0 is not prev:
                self.dfs(n0, path)
            elif n1.count > 0 and n1 is not prev:
                self.dfs(n1, path)
        elif len(curr.neighbors) == 4:
            # self-intersecting vertex
            # we need prev to determine the direction
            assert prev is not None
            for n in curr.neighbors:
                n: _Vertex = self.vertices[n]
                if n is prev:   # skip prev
                    continue
                cell_0 = self.edges[(prev.x, prev.y, curr.x, curr.y)].cell_pos
                cell_1 = self.edges[(curr.x, curr.y, n.x, n.y)].cell_pos
                if cell_0 == cell_1:
                    # print((prev.x, prev.y), (curr.x, curr.y), (n.x, n.y))
                    if n.count > 0:
                        self.dfs(n, path)
                    return
            # no neighbor is available
            raise ValueError('a self-intersecting vertex has no valid neighbor')

    def polygon_area(self, path: list[_Vertex]) -> float:
        """shoelace formula"""
        area = 0.0
        for i in range(len(path)):
            p1 = path[i]
            p2 = path[(i+1) % len(path)]
            area += (p1.x*p2.y - p2.x*p1.y)
        return area / 2.0

    def solve(self) -> list[list[_Vertex]]:
        res = []
        for v in self.vertices.values():
            # never use self-intersecting vertex as start
            if len(v.neighbors) == 4:
                continue
            if v.count == 1:
                path: list[_Vertex] = []
                self.dfs(v, path)
                assert len(path) >= 3
                # determine the order of the path
                # get the most top-left vertex
                topleft = path[0]
                for p in path:
                    if p.y < topleft.y or (p.y == topleft.y and p.x < topleft.x):
                        topleft = p
                # first make sure all the path are in the same order
                if self.polygon_area(path) < 0:
                    path.reverse()
                # if it is a hole, reverse it
                if not self.map.has_cell(topleft.x, topleft.y):
                    path.reverse()
                
                # simplify the path
                path = simplify(path)
                res.append(path)
        return res
    
    def add_edge(self, x, y, z, w, cell_pos: tuple[int, int]):
        t0 = (x, y, z, w)
        t1 = (z, w, x, y)
        self.edges[t0].count += 1
        self.edges[t1].count += 1
        self.edges[t0].cell_pos = cell_pos
        self.edges[t1].cell_pos = cell_pos

class Tilemap(Node):
    def __init__(self, layer: AutoTiledLayer, name=None, parent=None):
        self.layer = layer
        self.data = layer.intGridCsv
        self.width = layer.width
        self.height = layer.height
        self.tiles = layer.bake_auto_layer_tiles()
        self.render_offset_y = layer.render_offset_y

        self.grid_size = self.layer.grid_size
        self.cell_size = self.layer.grid_size / _g.PIXEL_PER_UNIT

        self.material = _g.default_material

        super().__init__(name, parent)

    tex: rl.Texture2D
    shader: rl.Shader
    b2_bodies: list[box2d.Body]

    def on_ready(self):
        self.tex = rl.LoadTexture("assets/" + self.layer.get_tileset_def().relPath)
        # self.shader = rl.LoadShaderFromMemory(PIXEL_SNAP_SHADER, None)

    def on_destroy(self):
        rl.UnloadTexture(self.tex)
        # rl.UnloadShader(self.shader)    # TODO: use static shader
    
    def has_cell(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return bool(self.data[x, y])
    
    def world_to_cell(self, pos: vec2) -> tuple[int, int]:
        transform = ~self.transform()
        pos = transform.transform_point(pos)
        pos /= self.cell_size
        return round(pos.x - 0.5), round(pos.y - 0.5)
    
    def cell_to_world(self, cx: int, cy: int) -> vec2:
        """Get world position of a cell's center"""
        transform = self.transform()
        pos = vec2(cx + 0.5, cy + 0.5) * self.cell_size
        return transform.transform_point(pos)

    def on_render(self):
        # rl.BeginShaderMode(self.shader)
        with self.material:
            self.draw(self.transform())
        # rl.EndShaderMode()
        # draw_circle(self.global_position, 0.2, Colors.Red)

    def draw(self, transform: mat3x3):
        w2v = _g.world_to_viewport
        scale = (w2v @ transform)._s() / _g.PIXEL_PER_UNIT

        bound_x_min = -_g.viewport_width * 0.5
        bound_x_max = _g.viewport_width * 1.5
        bound_y_min = -_g.viewport_height * 0.5
        bound_y_max = _g.viewport_height * 1.5

        for x, y, info in self.tiles:
            y += self.render_offset_y
            pos = vec2(x, y) * self.cell_size
            # optimized draw_sprite
            pos = w2v.transform_point(transform.transform_point(pos))

            # if pos is far away from the screen, skip it
            if pos.x<bound_x_min or pos.x>bound_x_max or pos.y<bound_y_min or pos.y>bound_y_max:
                continue

            src_rect = rl.Rectangle(info.srcX, info.srcY, self.grid_size, self.grid_size)
            dest_width = src_rect.width * scale.x
            dest_height = src_rect.height * scale.y
            if info.flips & 0b01:   # flip_x
                src_rect.width *= -1
            if info.flips & 0b10:   # flip_y
                src_rect.height *= -1
            dest_rect = rl.Rectangle(pos.x, pos.y, dest_width, dest_height)
            rl.DrawTexturePro(self.tex, src_rect, dest_rect, vec2(0, 0), 0, Colors.White)

    def bake_box2d_bodies(self, node: Node, optimize=True) -> list[box2d.Body]:
        bodies = []
        transform = node.transform()
        scale = transform._s()
        cell_extent = scale * self.cell_size / 2

        for y in range(self.height):
            body: box2d.Body = None
            merged_init_pos: vec2 = None
            merged_count = 1
            for x in range(self.width):
                if self.data[x, y] != 1:
                    continue
                pos = vec2(x, y) * self.cell_size

                curr_pos = transform.transform_point(pos) + cell_extent
                if optimize:
                    if x > 0 and self.data[x-1, y] == 1:
                        merged_count += 1
                        # update position and size
                        body.position = (merged_init_pos + curr_pos) / 2
                        body.set_box_shape(cell_extent.x * merged_count, cell_extent.y)
                        continue
                    else:
                        merged_count = 1

                body = node.create_body()
                body.type = 0
                body.position = curr_pos
                merged_init_pos = curr_pos
                body.set_box_shape(cell_extent.x, cell_extent.y)
                bodies.append(body)
        return bodies

    def bake_box2d_bodies_chain(self, node: Node) -> list[box2d.Body]:
        res = _TilemapColliderSolver(self).solve()
        bodies = []
        transform = node.transform()
        for path in res:
            body = node.create_body()
            body.type = 0   # static
            vertices = []
            for v in path:
                pos = vec2(v.x, v.y) * self.cell_size
                vertices.append(transform.transform_point(pos))
            body.set_chain_shape(vertices)
            bodies.append(body)
        return bodies