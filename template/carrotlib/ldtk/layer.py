from .project import Project
from .defs.rule import AutoLayerRuleDef
from .defs.layer import AutoTiledLayerDef

from array2d import array2d

class TileInfo:
    def __init__(self, x: int, y: int, srcX: int, srcY: int, tid: int, flips: int, a: float):
        self.x = x
        self.y = y
        self.srcX = srcX
        self.srcY = srcY
        self.tid = tid
        self.flips = flips
        self.a = a

# Map<Int, Map<Int, Array<{x:Int, y:Int, flips:Int, srcX:Int, srcY:Int, tid:Int, a:Float}>>>
AutoTilesCache = dict[
    int,                            # rule uid
    dict[
        tuple[int, int],            # coord
        list[TileInfo]          # tiles
    ]     
]

class AutoTiledLayer:
    intGridCsv: array2d[int]
    seed: int
    definition: AutoTiledLayerDef

    def __init__(self, level: dict, index: int, project: Project) -> None:
        self.data = level['layerInstances'][index]
        self.project = project
        self.seed = self.data['seed']
        self.definition = self.project.get_layer_def(self.data['layerDefUid'])

        if self.data['__type'] == 'IntGrid':
            pass
        elif self.data['__type'] == 'AutoLayer':
            self.data = self.data.copy()
            autoSourceLayerDefUid = self.definition.autoSourceLayerDefUid
            assert autoSourceLayerDefUid is not None
            # find intGridCsv
            for layer in level['layerInstances']:
                if layer['layerDefUid'] == autoSourceLayerDefUid:
                    self.data['intGridCsv'] = layer['intGridCsv']
                    break
            else:
                raise Exception(f"cannot find 'intGridCsv' with autoSourceLayerDefUid={autoSourceLayerDefUid}")
        else:
            raise Exception(f'unsupported type: {self.data["__type"]}')

        self.intGridCsv = array2d(self.data['__cWid'], self.data['__cHei'])
        self.intGridCsv.copy_(self.data['intGridCsv'])

    @property
    def render_offset_y(self) -> int:
        return self.data['__pxTotalOffsetY'] // self.grid_size

    @property
    def width(self) -> int:
        return self.intGridCsv.width
    
    @property
    def height(self) -> int:
        return self.intGridCsv.height
    
    @property
    def grid_size(self) -> int:
        return self.data['__gridSize']
    
    def get_tileset_def(self):
        return self.project.get_tileset_def(self.data['__tilesetDefUid'])

    def is_valid(self, cx: int, cy: int):
        return self.intGridCsv.is_valid(cx, cy)

    def get_IntGrid(self, cx: int, cy: int, default=0) -> int:
        return self.intGridCsv.get(cx, cy, default)

    def bake_ldtk_auto_layer_tiles(self) -> list[dict]:
        """generate a LDtk compatible array of tiles"""
        arr = []
        cache = self.apply_rules()
        rules = self.definition.get_active_rules()
        rules.reverse() # in display order
        for r in rules:
            if r.uid not in cache:
                continue
            for key, value in cache[r.uid].items():
                ckey = key[0] + key[1] * self.width
                for info in value:
                    arr.append({
                        'px': (info.x, info.y),         # pixel coords in layer
                        'src': (info.srcX, info.srcY),  # pixel coords in tileset
                        'f': info.flips,                # flip flags
                        't': info.tid,                  # tile id
                        'd': (r.uid, ckey),             # rule uid, coord id
                        'a': r.alpha                    # rule alpha
                    })
        return arr
    
    def bake_auto_layer_tiles(self) -> list[tuple[int, int, TileInfo]]:
        """generate a 2D array of tile ids"""
        tiles = []
        cache = self.apply_rules()
        rules = self.definition.get_active_rules()
        rules.reverse() # in display order
        for r in rules:
            if r.uid not in cache:
                continue
            for key, value in cache[r.uid].items():
                cx, cy = key
                for info in value:
                    tiles.append((cx, cy, info))
        return tiles

    def apply_rules(self) -> AutoTilesCache:
        output: AutoTilesCache = {}
        # Apply rules
        source = self
        for rule in self.definition.get_active_rules():
            for x in range(self.width):
                for y in range(self.height):
                    self.apply_rule_at(output, source, rule, x, y)

        # Discard using break-on-match flag
        self.apply_break_on_matches_area(output)
        return output

    def apply_break_on_matches_area(self, output: AutoTilesCache) -> None:
        coord_locks = set()
        td = self.get_tileset_def()
        active_rules = self.definition.get_active_rules()

        for y in range(self.height):
            for x in range(self.width):
                for rule in active_rules:
                    output_i = output.get(rule.uid)
                    if output_i is None:
                        continue
                    output_ij = output_i.get((x, y))
                    if output_ij is None:
                        continue

                    if (x, y) in coord_locks:
                        # Tiles below locks are discarded
                        output_i.pop((x, y))
                    elif rule.breakOnMatch:
                        # Break on match is ON
                        coord_locks.add((x, y))
                    elif not rule.hasAnyPositionOffset() and rule.alpha >= 1:
                        # Check for opaque tiles
                        for t in output_ij:
                            if td.isTileOpaque(t.tid):
                                coord_locks.add((x, y))
                                break
    
    def apply_rule_at(self, output: AutoTilesCache, source: 'AutoTiledLayer', r: AutoLayerRuleDef, cx: int, cy: int):
        # Init
        if r.uid not in output:
            output[r.uid] = {}
        output_i = output[r.uid]
        output_i.pop((cx, cy), None)

        # Modulos
        if r.checker != 'Vertical' and (cy - r.yOffset) % r.yModulo != 0:
            return False
        
        if r.checker == 'Vertical' and (cy + (cx // r.xModulo) % 2) % r.yModulo != 0:
            return False
        
        if r.checker != 'Horizontal' and (cx - r.xOffset) % r.xModulo != 0:
            return False
        
        if r.checker == 'Horizontal' and (cx + (cy // r.yModulo) % 2) % r.xModulo != 0:
            return False
    
        # Apply rule
        matched = False
        if r.matches(self, source, cx, cy):
            self.add_rule_tiles_at(output_i, r, cx, cy, 0)
            matched = True

        if (not matched or not r.breakOnMatch) and r.flipX and r.matches(self, source, cx, cy, -1):
            self.add_rule_tiles_at(output_i, r, cx, cy, 1)
            matched = True

        if (not matched or not r.breakOnMatch) and r.flipY and r.matches(self, source, cx, cy, 1, -1):
            self.add_rule_tiles_at(output_i, r, cx, cy, 2)
            matched = True

        if (not matched or not r.breakOnMatch) and r.flipX and r.flipY and r.matches(self, source, cx, cy, -1, -1):
            self.add_rule_tiles_at(output_i, r, cx, cy, 3)
            matched = True

        return matched
    
    def add_rule_tiles_at(self, output_i: dict, r: AutoLayerRuleDef, cx: int, cy: int, flips: int) -> None:
        td = self.get_tileset_def()
        
        if r.tileMode == 'Single':
            tile_rect_ids = r.getRandomTileRectIdsForCoord(self.seed, cx, cy, flips)
            stamp_infos = None
        else:
            tile_rect_ids = r.tileRectsIds
            # stamp_infos = getRuleStampRenderInfos(r, td, tileIds, flips);
            raise NotImplementedError

        if (cx, cy) not in output_i:
            output_i[(cx, cy)] = []

        output_ij = output_i[(cx, cy)]

        def_gridSize = self.data['__gridSize']
        assert stamp_infos is None

        for tid in tile_rect_ids:
            output_ij.append(TileInfo(
                cx * def_gridSize + r.getXOffsetForCoord(self.seed, cx, cy, flips),
                cy * def_gridSize + r.getYOffsetForCoord(self.seed, cx, cy, flips),
                td.getTileSourceX(tid), # srcX
                td.getTileSourceY(tid), # srcY
                tid,
                flips,
                r.alpha
            ))
