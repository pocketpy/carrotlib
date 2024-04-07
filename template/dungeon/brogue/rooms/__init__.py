from array2d import array2d
import random
from .utils import brogue_chooseRandomDoorSites, brogue_attachHallwayTo
from .simple import brogue_designChunkyRoom, brogue_designCircularRoom, brogue_designCrossRoom, brogue_designEntranceRoom, brogue_designSmallRoom, brogue_designSymmetricalCrossRoom
from .cavern import brogue_design_cave, brogue_design_compat_cavern, brogue_design_large_east_west_cavern, brogue_design_large_north_south_cavern

'''
所有的房间主体形状的生成算法分布在 .cavern.py 和 .simple.py 中
与房间生成相关的算法在 .utils.py 中
'''


# 所有房间生成算法的调用者, 将根据房间生成权重数组从所有房间中随机选择一个生成, 并生成走廊并返回走廊出口----------------------------
def brogue_designRandomRoom(grid: array2d[int], room_type_frequencies=(1,1,1,1,1,1,1,1), has_doors=True, has_hallway=True) -> list[tuple[int, int] | None]:
    '''
    在空的grid中就地生成一个随机的房间, 附加上走廊并返回走廊出口
    
    Args:
        grid (array2d[int]): 二维数组表示地图的网格，应当为地牢的总地图尺寸。
        has_doors (bool): 是否生成门
        has_hallway (bool): 是否生成走廊(只有当有has_doors为True时才有效)
        room_type_frequencies (list[float, ROOM_TYPE_COUNT]): 一个长度为ROOM_TYPE_COUNT的列表, 表示每种房间的生成概率权重, 每个权重的值大于等于0即可
    Returns:
        (list[list[int, 2], 4]): 表示 走廊出口/门 的位置
    '''
    room_type_func_list = room_type_func_list = [
        "brogue_designCrossRoom",
        "brogue_designSymmetricalCrossRoom",
        "brogue_designSmallRoom",
        "brogue_designCircularRoom",
        "brogue_designChunkyRoom",
        [
            "brogue_design_compat_cavern",
            "brogue_design_large_north_south_cavern",
            "brogue_design_large_east_west_cavern",
        ],
        "brogue_design_cave",
        "brogue_designEntranceRoom"
    ]
    # 按权重选取房间生成函数
    f = random.choices(room_type_func_list, room_type_frequencies)[0]
    # 选中了cavern, 那么进一步选择生成什么cavern
    if isinstance(f, list):
        f = random.choice(f)
    
    # 生成房间
    if f == "brogue_designCrossRoom":
        brogue_designCrossRoom(grid)
    elif f == "brogue_designSymmetricalCrossRoom":
        brogue_designSymmetricalCrossRoom(grid)
    elif f == "brogue_designSmallRoom":
        brogue_designSmallRoom(grid)
    elif f == "brogue_designCircularRoom":
        brogue_designCircularRoom(grid)
    elif f == "brogue_designChunkyRoom":
        brogue_designChunkyRoom(grid)
    elif f == "brogue_design_cave":
        brogue_design_cave(grid)
    elif f == "brogue_designEntranceRoom":
        brogue_designEntranceRoom(grid)
    elif f == "brogue_design_compat_cavern":
        brogue_design_compat_cavern(grid)
    elif f == "brogue_design_large_north_south_cavern":
        brogue_design_large_north_south_cavern(grid)
    elif f == "brogue_design_large_east_west_cavern":
        brogue_design_large_east_west_cavern(grid)
    else:
        assert False
        
    # 生成门
    door_positions = [None] * 4
    if has_doors:
        door_positions = brogue_chooseRandomDoorSites(grid)
        
        # 生成走廊
        if has_hallway:
            door_positions = brogue_attachHallwayTo(grid, door_positions)
            
    return door_positions