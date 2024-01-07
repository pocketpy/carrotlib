from typing import Optional, TYPE_CHECKING
from ..perlin import Perlin

if TYPE_CHECKING:
    from ldtk.layer import AutoTiledLayer
    from ldtk.defs.layer import AutoTiledLayerDef

def _rand_seed_coords(seed: int, x: int, y: int, max: int):
    # Source: https://stackoverflow.com/questions/37128451/random-number-generator-with-x-y-coordinates-as-seed
    h = seed + x*374761393 + y*668265263; # all constants are prime
    h = (h^(h >> 13)) * 1274126177
    return ( h^(h >> 16) ) % max

class Const:
    AUTO_LAYER_ANYTHING = 1000001
    MAX_AUTO_PATTERN_SIZE = 7

class AutoLayerRuleDef:
    uid: int

    tileIds: list[int] = []
    chance: float = 1.0
    breakOnMatch: bool = True
    size: int
    pattern: list[int] = []
    alpha: float = 1.0
    outOfBoundsValue: Optional[int] = None
    flipX: bool = False
    flipY: bool = False
    active: bool = True
    tileMode: str = 'Single' # Single, Stamp
    pivotX: float = 0.0
    pivotY: float = 0.0
    xModulo: int = 1
    yModulo: int = 1
    xOffset: int = 0
    yOffset: int = 0
    tileXOffset: int = 0
    tileYOffset: int = 0
    tileRandomXMin: int = 0
    tileRandomXMax: int = 0
    tileRandomYMin: int = 0
    tileRandomYMax: int = 0
    checker: str = 'None'   # None, Horizontal, Vertical

    perlinActive: bool = False
    perlinSeed: int
    perlinScale: float = 0.2
    perlinOctaves: int = 2
    _perlin: Optional[Perlin] = None

    def __init__(self, data: dict):
        self.data = data
        fields = ['uid', 'tileIds', 'chance', 'breakOnMatch', 'size', 'pattern', 'alpha', 'outOfBoundsValue', 'flipX', 'flipY', 'active', 'tileMode', 'pivotX', 'pivotY', 'xModulo', 'yModulo', 'xOffset', 'yOffset', 'tileXOffset', 'tileYOffset', 'tileRandomXMin', 'tileRandomXMax', 'tileRandomYMin', 'tileRandomYMax', 'checker', 'perlinActive', 'perlinSeed', 'perlinScale', 'perlinOctaves']
        for field in fields:
            setattr(self, field, data[field])

    def has_any_position_offset(self) -> bool:
        return self.tileRandomXMin != 0 or self.tileRandomXMax != 0 or self.tileRandomYMin != 0 or self.tileRandomYMax != 0 or self.tileXOffset != 0 or self.tileYOffset != 0
    
    def is_valid_size(self, size: int) -> bool:
        return size >= 1 and size <= Const.MAX_AUTO_PATTERN_SIZE and size % 2 != 0
    
    @property
    def perlin(self) -> Perlin:
        if self.perlinSeed is not None and self._perlin is None:
            self._perlin = Perlin()
            self._perlin.normalize = True
            self._perlin.adjustScale(50, 1)

        if self.perlinSeed is None and self._perlin is not None:
            self._perlin = None
        
        return self._perlin
    
    def has_perlin(self) -> bool:
        return self.perlinActive
    
    def set_perlin(self, active: bool):
        if not active:
            self.perlinActive = False
            self._perlin = None
        else:
            self.perlinActive = True

    def is_symetric_x(self) -> bool:
        for cx in range(self.size // 2):
            for cy in range(self.size):
                if self.pattern[self.coord_id(cx, cy)] != self.pattern[self.coord_id(self.size-1-cx, cy)]:
                    return False
        
        return True
    
    def is_symetric_y(self) -> bool:
        for cx in range(self.size):
            for cy in range(self.size // 2):
                if self.pattern[self.coord_id(cx, cy)] != self.pattern[self.coord_id(cx, self.size-1-cy)]:
                    return False
        
        return True
    
    def get(self, cx: int, cy: int) -> int:
        return self.pattern[self.coord_id(cx, cy)]
    
    def set(self, cx: int, cy: int, v: int) -> None:
        if self.is_valid(cx, cy):
            self.pattern[self.coord_id(cx, cy)] = v
        
    def fill(self, v: int):
        for cx in range(self.size):
            for cy in range(self.size):
                self.set(cx, cy, v)

    def init_pattern(self):
        self.pattern = [0] * (self.size * self.size)

    def __str__(self):
        return f"Rule#{self.uid}({self.size}x{self.size})"

    def resize(self, newSize: int):
        if not self.is_valid_size(newSize):
            raise ValueError(f"Invalid rule size {self.size}x{self.size}")
        
        oldSize = self.size
        oldPatt = self.pattern.copy()
        pad = abs(newSize-oldSize) // 2

        self.size = newSize
        self.init_pattern()
        if newSize < oldSize:
            # Decrease
            for cx in range(newSize):
                for cy in range(newSize):
                    self.pattern[cx + cy*newSize] = oldPatt[cx+pad + (cy+pad)*oldSize]
        else:
            # Increase
            for cx in range(oldSize):
                for cy in range(oldSize):
                    self.pattern[cx+pad + (cy+pad)*newSize] = oldPatt[cx + cy*oldSize]

    def coord_id(self, cx: int, cy: int) -> int:
        return cx + cy*self.size
    
    def is_valid(self, cx: int, cy: int) -> bool:
        return (0 <= cx < self.size) and (0 <= cy < self.size)
    
    def trim(self) -> bool:
        while self.size > 1:
            emptyBorder = True
            for cx in range(self.size):
                if self.pattern[self.coord_id(cx, 0)] != 0 or self.pattern[self.coord_id(cx, self.size-1)] != 0:
                    emptyBorder = False
                    break
            for cy in range(0, self.size):
                if self.pattern[self.coord_id(0, cy)] != 0 or self.pattern[self.coord_id(self.size-1, cy)] != 0:
                    emptyBorder = False
                    break
            
            if emptyBorder:
                self.resize(self.size-2)
            else:
                return False
        
        return True
    
    def is_empty(self) -> bool:
        for v in self.pattern:
            if v != 0:
                return False
        
        return len(self.tileIds) == 0
    
    def is_using_unknown_IntGrid_values(self, ld: 'AutoTiledLayerDef'):
        raise NotImplementedError
    
    def matches(self, li: 'AutoTiledLayer', source: 'AutoTiledLayer', cx: int, cy: int, dirX: int = 1, dirY: int = 1) -> bool:
        if len(self.tileIds) == 0:
            return False
        
        if self.chance<=0 or (self.chance<1 and _rand_seed_coords(li.seed+self.uid, cx, cy, 100)>=self.chance*100):
            return False
        
        if self.has_perlin() and self.perlin.perlin(li.seed+self.perlinSeed, cx*self.perlinScale, cy*self.perlinScale, self.perlinOctaves)<0:
            return False
        
        # Rule check
        value: Optional[int] = 0
        radius = self.size // 2
        for px in range(self.size):
            for py in range(self.size):
                coordId = px + py*self.size
                if self.pattern[coordId] == 0:
                    continue

                value = source.get_IntGrid(
                    cx+dirX*(px-radius),
                    cy+dirY*(py-radius),
                    default=self.outOfBoundsValue
                )
                
                if value is None:
                    return False
                
                if abs(self.pattern[coordId]) == Const.AUTO_LAYER_ANYTHING:
                    # "Anything" checks
                    if self.pattern[coordId] > 0 and value == 0:
                        return False
                    
                    if self.pattern[coordId] < 0 and value != 0:
                        return False
                elif abs(self.pattern[coordId]) > 999:
                    # Group checks
                    raise NotImplementedError
                else:
                    # Specific value checks
                    if self.pattern[coordId] > 0 and value != self.pattern[coordId]:
                        return False
                    
                    if self.pattern[coordId] < 0 and value == -self.pattern[coordId]:
                        return False
        
        return True
    
    def tidy(self, ld: 'AutoTiledLayerDef'):
        raise NotImplementedError
    
    def get_random_tile_for_coord(self, seed: int, cx: int, cy: int, flips: int) -> int:
        index = _rand_seed_coords(self.uid+seed+flips, cx, cy, len(self.tileIds))
        return self.tileIds[index]
    
    def get_x_offset_for_coord(self, seed: int, cx: int, cy: int, flips: int) -> int:
        _0 = 1 if flips & 1 else -1
        if self.tileRandomXMin == 0 and self.tileRandomXMax == 0:
            _1 = 0
        else:
            _1 = _rand_seed_coords(self.uid+seed+flips, cx, cy, self.tileRandomXMax-self.tileRandomXMin+1) + self.tileRandomXMin
        return _0 * (self.tileXOffset + _1)

    def get_y_offset_for_coord(self, seed: int, cx: int, cy: int, flips: int) -> int:
        _0 = 1 if flips & 2 else -1
        if self.tileRandomYMin == 0 and self.tileRandomYMax == 0:
            _1 = 0
        else:
            _1 = _rand_seed_coords(self.uid+seed+1, cx, cy, self.tileRandomYMax-self.tileRandomYMin+1) + self.tileRandomYMin
        return _0 * (self.tileYOffset + _1)
