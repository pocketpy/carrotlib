'''
定义一些常量
'''



'''
下面是Rooms.py的常量,用于控制单个房间的生成
'''
# 使用全局常量来表示格子的填充值，方便以后统一修改
ONE = 1
ZERO = 0
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
NINE = 9
# 地牢的总的地图的尺寸, 原作设定是(w:79, h:29)
DUNGEON_WIDTH = 79  
DUNGEON_HEIGHT = 29
# 垂直/水平方向的房间走廊的长度区间, 原作设定是(水平:5~15, 垂直:2~9)
HORIZONTAL_CORRIDOR_MIN_LENGTH = 5
HORIZONTAL_CORRIDOR_MAX_LENGTH = 15
VERTICAL_CORRIDOR_MIN_LENGTH = 2
VERTICAL_CORRIDOR_MAX_LENGTH = 9
# 房间类型的数量, 原作设定是8, 即一共存在8种样式的房间
ROOM_TYPE_COUNT = 8
# 超大洞穴类型房间的最小规格
CAVE_MIN_WIDTH = 50
CAVE_MIN_HEIGHT = 20

# attachRooms中生成房间的总尝试次数和房间的最大数量, 原作设定是(总尝试次数<=35, 生成的总数量<=35)
ATTACH_ROOMS_ATTEMPT_COUNT = 35
ATTACH_ROOMS_MAX_COUNT = 35

IS_DEBUG = True


'''
下面是Level.py的常量,用于控制一层的生成
'''
# from abc import abstractmethod


class DungeonProfile:
    '''
    房间的生成概率配置类, 它决定了该房间的样式
    '''
    room_frequencies: list[float]  # 房间生成概率列表
    corridor_chance: float  # 走廊的生成概率 0~100
    def __init__(self, depth_level, amulet_level):

        self._set_basics()
        self._initialize_by_depth(depth_level, amulet_level)

    # @ abstractmethod
    def _set_basics(self):
        pass
    
    def _initialize_by_depth(self, depth_level, amulet_level):
        """
        按照层数设定房间生成概率和走廊生成概率
        """
        interpreted_depth = 100 * (depth_level - 1) / amulet_level if depth_level > 1 else 0
        descent_percent = 100 if interpreted_depth > 100 else interpreted_depth
        
        self.room_frequencies[0] += 20 * (100 - descent_percent) / 100
        self.room_frequencies[1] += 10 * (100 - descent_percent) / 100
        self.room_frequencies[3] +=  7 * (100 - descent_percent) / 100
        self.room_frequencies[5] += 10 * descent_percent / 100
        
        self.corridor_chance = self.corridor_chance + 80 * (100 - descent_percent) / 100
        

class DungeonProfileForBasicRooms(DungeonProfile):
    '''
    地牢在大多数的基本房间的生成概率配置类
    '''
    def _set_basics(self):
        # 此处设置基础概率, 之后会根据地牢深度进行调整
        #
        #  0: 十字房间 (Cross room)
        #  1: 小型对称十字房间 (Small symmetrical cross room)
        #  2: 小房间 (Small room)
        #  3: 圆形房间 (Circular room)
        #  4: 不规则块状房间 (Chunky room)
        #  5: 洞穴 (各种Cave)
        #  6: 巨大洞穴 (填满整个地下层的那种大洞穴，Cavern)
        #  7: 入口房间 (位于第一层的大倒 “T” 形房间，Entrance room)
        #  ||
        #  ||
        #  L=====>               0   1   2   3   4   5   6   7   
        self.room_frequencies = [2,  1,  1,  1,  7,  1,  0,  0]
        self.corridor_chance = 10  # 意味将有10%的概率生成走廊,也就是说再在附近生成新的房间

class DungeonProfileForFirstRooms(DungeonProfile):
    '''
    每一层的第一个房间的生成概率配置类
    '''
    def _set_basics(self):
        # 此处设置基础概率, 之后会根据地牢深度进行调整
        #
        #  0: 十字房间 (Cross room)
        #  1: 小型对称十字房间 (Small symmetrical cross room)
        #  2: 小房间 (Small room)
        #  3: 圆形房间 (Circular room)
        #  4: 不规则块状房间 (Chunky room)
        #  5: 洞穴 (各种Cave)
        #  6: 巨大洞穴 (填满整个地下层的那种大洞穴，Cavern)
        #  7: 入口房间 (位于第一层的大倒 “T” 形房间，Entrance room)
        #  ||
        #  ||
        #  L=====>               0   1   2   3   4   5   6   7   
        self.room_frequencies = [10, 0,  0,  3,  7,  10, 10, 0]
        self.corridor_chance = 0

class DungeonProfileForGoblinWarrens(DungeonProfile):
    '''
    哥布林地洞房间的生成概率配置类
    '''
    def _set_basics(self):
        # 此处设置基础概率, 之后会根据地牢深度进行调整
        #
        #  0: 十字房间 (Cross room)
        #  1: 小型对称十字房间 (Small symmetrical cross room)
        #  2: 小房间 (Small room)
        #  3: 圆形房间 (Circular room)
        #  4: 不规则块状房间 (Chunky room)
        #  5: 洞穴 (各种Cave)
        #  6: 巨大洞穴 (填满整个地下层的那种大洞穴，Cavern)
        #  7: 入口房间 (位于第一层的大倒 “T” 形房间，Entrance room)
        #  ||
        #  ||
        #  L=====>               0   1   2   3   4   5   6   7   
        self.room_frequencies = [0,  0,  1,  0,  0,  0,  0,  0]
        self.corridor_chance = 0

class DungeonProfileForSentinelSanctuaries(DungeonProfile):
    '''
    哨兵圣所房间的生成概率配置类
    '''
    def _set_basics(self):
        # 此处设置基础概率, 之后会根据地牢深度进行调整
        #
        #  0: 十字房间 (Cross room)
        #  1: 小型对称十字房间 (Small symmetrical cross room)
        #  2: 小房间 (Small room)
        #  3: 圆形房间 (Circular room)
        #  4: 不规则块状房间 (Chunky room)
        #  5: 洞穴 (各种Cave)
        #  6: 巨大洞穴 (填满整个地下层的那种大洞穴，Cavern)
        #  7: 入口房间 (位于第一层的大倒 “T” 形房间，Entrance room)
        #  ||
        #  ||
        #  L=====>               0   1   2   3   4   5   6   7   
        self.room_frequencies = [0,  5,  0,  1,  0,  0,  0,  0]
        self.corridor_chance = 0

DIRS_4 = [(0, -1), (0, 1), (-1, 0), (1, 0)]
