from array2d import array2d
from typing import Literal
from dungeon.brogue.const import *

"""生成门的四种情况
上(0)   下(1)   左(2)   右(3)
? . ?   ? 1 ?   ? . ?   ? . ?
. . .   . . .   . . 1   1 . .
? 1 ?   ? . ?   ? . ?   ? . ?
"""
# 我倾向于让对侧的门满足某种数学关系，例如 (i+2)%4

class DoorTester:
    def __init__(self, grid: array2d[int]):
        self.grid = grid

        self.grid_neighbors_ZERO = grid.count_neighbors(ZERO, 'von Neumann')
        self.grid_neighbors_ONE = grid.count_neighbors(ONE, 'von Neumann')
        self.grid_neighbors_TWO = grid.count_neighbors(TWO, 'Moore')

    def test(self, x: int, y: int) -> Literal[-1, 0, 1, 2, 3]:
        # 目标点必须是 ZERO
        if self.grid.get(x, y) != ZERO:
            return -1
        # 目标点的 4-邻域中必须有且仅有一个 ONE
        if self.grid_neighbors_ONE[x, y] != 1:
            return -1
        # 目标点的 4-邻域中必须有且仅有三个 ZERO
        if self.grid_neighbors_ZERO[x, y] != 3:
            return -1
        # 目标点的 8-邻域中不能有 TWO
        # TODO: 支持半径设置，以免门之间过于紧密
        if self.grid_neighbors_TWO[x, y] > 0:
            return -1
        
        if self.grid[x, y+1] == ONE:
            return 0
        if self.grid[x, y-1] == ONE:
            return 1
        if self.grid[x+1, y] == ONE:
            return 2
        if self.grid[x-1, y] == ONE:
            return 3
