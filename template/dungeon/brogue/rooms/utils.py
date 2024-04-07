from array2d import array2d
import random

from dungeon.brogue.const import *
from dungeon.brogue.doors import DoorTester

'''
utils.py 包含了生成房间的小部分相关算法
'''

# 在本文件中, 完全复刻自brogue的算法将使用 "brogue_<brogue中该函数的原名>" 命名
def clamp(x, a, b):
    if a > b: a, b = b, a
    if x < a: return a
    if x > b: return b
    return x


def brogue_chooseRandomDoorSites(grid: array2d[int]) -> list[tuple[int, int] | None]:
    '''
    对于上下左右四个方向, 在提供的房间grid中, 分别寻找1个能够满足"可以向本方向打开门"的格子的位置, 当某个方向找不到符合要求的格子时, 将使用`None`表示
    
    - 对于"可以向本方向打开门"的判断标准:
        - 1. 需要首先满足 brogue_directionOfDoorSite 中对格子的要求
        - 2. 其次需要保证向门打开的方向上延伸10格, 不能遇到房间格子
    '''
    door_tester = DoorTester(grid)
    results: list[list[tuple[int, int]]] = [[] for _ in range(4)]
    for y in range(grid.height):
        for x in range(grid.width):
            # 首先判断本格是否满足"可以向本方向打开门"的判断标准的第一点
            direction_index = door_tester.test(x, y)
            if direction_index == -1:  # no direction  表示本格无法满足条件
                continue
            
            # 下面的循环会判断是否满足标准的第二点
            direction_delta_x, direction_delta_y = DIRS_4[direction_index]

            can_open = True
            for detect_length in range(1, 10+1):
                # 将门打开的方向(通过第一重判断得到的direction_index)作为探测方向依次延申10格
                detect_x = x + detect_length * direction_delta_x
                detect_y = y + detect_length * direction_delta_y
                # 忽略出界的探测点
                if not grid.is_valid(detect_x, detect_y):
                    break
                # 如果发现探测途中遇到了房间格子, 则说明无法向该方向打开门
                if grid[detect_x, detect_y] != ZERO:
                    can_open = False
                    break
            
            # 标记完全符合判断标准的位置为可以打开门的方向的标签
            if can_open:
                results[direction_index].append((x, y))
    
    ret = [None] * 4
    for i, r in enumerate(results):
        if r:
            ret[i] = random.choice(r)
    return ret


def brogue_attachHallwayTo(grid: array2d[int], door_positions: list[tuple[int, int] | None]) -> list[tuple[int, int] | None]:
    '''
    在grid上绘制走廊。并返回走廊的出口坐标, 大多数情况下出口坐标会是在走廊方向继续延伸一格的位置, 在小部分情况下(15%)会返回排除走廊延伸方向的对向方向外的其余3个方向上的坐标
    ```
    如算法选择了door_positions中表示向右打开的门,并生成了走廊:  #表示房间, +表示走廊, 实际上它们的存储值都是1,但这里使用不同的符号加以区分
        # #
        # # + + + + + 
        # #
    此时算法将返回的位置绝大多数是:
        # #
        # # + + + + + @ <---- @表示出口,假设此处坐标是(3, 4), 而因为它向右侧延伸,因此返回值是[None, None, None, (3, 4)]
        # #
    有小部分情况下是:
        # #         @
        # # + + + + + @ <---- 返回值是[(2, 3), (2, 5), (3, 4), None]
        # #         @
    ```
    Args:
        grid (array2d[int]): 二维数组表示地图的网格，应当为地牢的总地图尺寸。
        door_positions: 4个方向的门的位置列表。
            一个包含4个二元列表的列表，每个二元列表分别表示朝向"上,下,左,右"打开的门的位置。
            当门的位置为 None 时表示没有朝向该方向打开的门。
    Returns:
        4个方向的走廊出口的位置列表。
        
    '''
    # 要求传入的grid的尺寸必须与总的地牢的地图尺寸一致
    assert grid.width == DUNGEON_WIDTH and grid.height == DUNGEON_HEIGHT
    
    # 选择一个合适的方向
    enumerated_door_positions = list(enumerate(door_positions))
    random.shuffle(enumerated_door_positions)

    direction_index = -1  # -1表示没有找到合适的方向
    door_pos = None
    for _direction_index, _door_pos in enumerated_door_positions:
        # 首先排除没有门的方向的坐标
        if _door_pos is None:
            continue

        door_x, door_y = _door_pos
        
        # 探测当前开门方向上将生成走廊的最远位置,是否超出了地图边界
        direction_delta_x, direction_delta_y = DIRS_4[_direction_index]
        detect_x = door_x + HORIZONTAL_CORRIDOR_MAX_LENGTH * direction_delta_x
        detect_y = door_y + VERTICAL_CORRIDOR_MAX_LENGTH * direction_delta_y
        
        if grid.is_valid(detect_x, detect_y):
            # 该方向上可以生成走廊
            direction_index = _direction_index
            door_pos = _door_pos
            break
    
    # 四个方向的门都不符合条件,那么就返回吧
    if direction_index == -1:
        return [None] * 4
    
    # 生成垂直方向的走廊
    if direction_index in (0, 1):  # 0,1表示"上,下"方向的direction_index
        corridor_length = random.randint(VERTICAL_CORRIDOR_MIN_LENGTH, VERTICAL_CORRIDOR_MAX_LENGTH)
    # 生成水平方向的走廊
    else:
        corridor_length = random.randint(HORIZONTAL_CORRIDOR_MIN_LENGTH, HORIZONTAL_CORRIDOR_MAX_LENGTH)
    
    # 绘制和房间相连的走廊, 走廊的地块使用1表示,和房间地块相同
    direction_delta_x, direction_delta_y = DIRS_4[_direction_index]

    start_x, start_y = door_pos
    end_x = start_x + direction_delta_x*(corridor_length-1)
    end_y = start_y + direction_delta_y*(corridor_length-1)
    
    step_x = -1 if end_x < start_x else 1
    step_y = -1 if end_y < start_y else 1

    for x in range(start_x, end_x+step_x, step_x):
        for y in range(start_y, end_y+step_y, step_y):
            grid[x, y] = ONE
    
    # 随机决定是否允许拐弯的走廊出口, 并更新走廊结束处的门位信息
    new_door_positions = door_positions.copy()
    end_x = clamp(end_x, 0, DUNGEON_WIDTH-1)
    end_y = clamp(end_y, 0, DUNGEON_HEIGHT-1)
    allow_oblique_hallway_exit = random.random() < 0.15  # 决定走廊出口是否允许拐弯
    
    for dir2, delta in enumerate(DIRS_4):
        new_x = end_x + delta[0]
        new_y = end_y + delta[1]

        if (dir2 != direction_index and not allow_oblique_hallway_exit) or grid.get(new_x, new_y) != ZERO:
            new_door_positions[dir2] = None
        else:
            new_door_positions[dir2] = new_x, new_y

    return new_door_positions 
