import random
from array2d import array2d

from dungeon.algorithm import canvas
from dungeon.brogue.const import *

'''
simple.py 集合了所有关于生成结构比较简单的房间的算法
'''


# 下面是生成房间的逻辑-------------------------------------------

def brogue_designCircularRoom(grid: array2d[int]):
    '''
    在grid中央上绘制一个圆形房间, 有大概率生成实心圆, 有小概率生成甜甜圈样式
    
    圆的半径在2~10之间
    '''
    assert grid.width >= 21 and grid.height >= 21 
    
    grid.fill_(ZERO)  # 以0填充所有的格子

    center_x = grid.width//2
    center_y = grid.height//2
    
    # 确定房间的半径
    if random.random() < 0.5:
        room_radius = random.randint(4, 10)
    else:
        room_radius = random.randint(2, 4)
    
    # 绘制房间
    canvas.fill_circle_(grid, ONE, center_x, center_y, room_radius)
    
    # 绘制房间中的空洞
    if room_radius > 6 and random.random() < 0.5:
        hole_radius = random.randint(3, room_radius-3)
        canvas.fill_circle_(grid, ZERO, center_x, center_y, hole_radius)


def brogue_designSmallRoom(grid: array2d[int]):
    '''
    在grid中央上绘制一个矩形房间
    
    矩形宽度在3~6之间, 高度在2~4之间
    '''
    assert grid.width >= 6 and grid.height >= 4 
    
    grid.fill_(ZERO)  # 以0填充所有的格子
    
    room_width = random.randint(3, 6)
    room_height = random.randint(2, 4)
    room_x = (grid.width - room_width) // 2  # 确保房间的中心和grid中心对齐
    room_y = (grid.height - room_height) // 2
    
    canvas.fill_rect_(grid, ONE, room_x, room_y, room_width, room_height)
    
    
def brogue_designCrossRoom(grid: array2d[int]):
    '''
    在房间偏左下的位置生成两个矩形交叉而成的房间
    '''
    assert grid.width >= 30 and grid.height >= 15
    grid.fill_(ZERO)  # 以0填充所有的格子

    # 确定两个房间的x坐标和宽度
    room1_width = random.randint(3, 12)
    room1_x =                                           \
        random.randint(
            max(0, grid.width//2 - (room1_width - 1)),
            grid.width//2
        )
    
    room2_width = random.randint(4, 20)
    room2_x =                                           \
        random.choice([-1, 0,0, 1,1,1, 2,2, 3]) +       \
        room1_x +                                       \
        (room1_width - room2_width)//2
    
    
    # 确定两个房间的y坐标和高度
    room1_height = random.randint(3, 7)
    room1_y = grid.height//2 - room1_height
    
    room2_height = random.randint(2, 5)
    room2_y =                                           \
        grid.height//2 -                                \
        room2_height +                                  \
        random.choice([0, -1,-1, -2,-2, -3])            
    
    # 将房间整体向左下角偏移
    room1_x -= 5
    room2_x -= 5
    room1_y += 5
    room2_y += 5
    
    # 绘制
    canvas.fill_rect_(grid, ONE, room1_x, room1_y, room1_width, room1_height)
    canvas.fill_rect_(grid, ONE, room2_x, room2_y, room2_width, room2_height)


def brogue_designSymmetricalCrossRoom(grid: array2d[int]):
    '''
    在房间中央生成两个矩形交叉而成的房间
    
    将不会生成"L"形房间
    '''
    assert grid.width >= 8 and grid.height >= 5 
    grid.fill_(ZERO)  # 以0填充所有的格子

    # 确定房间1的规格
    room1_width = random.randint(4, 8)
    room1_height = random.randint(4, 5)
    
    # 根据房间1规格的奇偶性, 确定房间2的规格, 为了避免生成"L"型房间
    room2_width = random.randint(3, 4) - 1 if room1_height % 2 == 0 else random.randint(3, 4)
    room2_height = 3 - 1 if room1_width % 2 == 0 else 3
    
    # 根据两个房间的规格, 确定格子的位置, 为了使得它们落在grid中央
    room1_x = (grid.width - room1_width) // 2
    room1_y = (grid.height - room1_height) // 2
    room2_x = (grid.width - room2_width) // 2
    room2_y = (grid.height - room2_height) // 2
    
    # 绘制
    canvas.fill_rect_(grid, ONE, room1_x, room1_y, room1_width, room1_height)
    canvas.fill_rect_(grid, ONE, room2_x, room2_y, room2_width, room2_height)


def brogue_designChunkyRoom(grid: array2d[int]):
    '''
    生成若干连续的小圆(下面称作chunk)拼成的房间, 首个圆生成在grid中央
    '''
    assert grid.width >= 14 and grid.height >= 15
    
    grid.fill_(ZERO) # 以0填充所有的格子

    chunk_count = random.randint(2, 8)  # 即将生成的小圆数量
    radius = 2  # 所有小圆的半径
    
    # 定义并绘制首个圆, 并寄存到表示"上一个圆"的变量
    last_circle = {
        'x': grid.width // 2, 
        'y': grid.height // 2,
        'next_min_x': grid.width // 2 - 3,  # 下一个圆的圆心随机生成范围
        'next_max_x': grid.width // 2 + 3,
        'next_min_y': grid.height // 2 - 3,
        'next_max_y': grid.height // 2 + 3,
    }
    canvas.fill_circle_(grid, ONE, last_circle['x'], last_circle['y'], radius)
    
    for _ in range(chunk_count):
        # 确定圆的位置, 必须让所有的圆的圆心落在已绘制的区域上
        while True:
            x = random.randint(last_circle['next_min_x'], last_circle['next_max_x'])
            y = random.randint(last_circle['next_min_y'], last_circle['next_max_y'])
            if grid[x,y] == 1:
                break
            
        
        # 确定当前的圆
        circle = {
            'x': x, 
            'y': y,
            'next_min_x': max(1, min(x-3, last_circle['next_min_x'])),
            'next_max_x': min(grid.width-2, max(x+3, last_circle['next_max_x'])),
            'next_min_y': max(1, min(y-3, last_circle['next_min_y'])),
            'next_max_y': min(grid.height-2, max(y+3, last_circle['next_max_y']))
        }
        
        last_circle = circle

        #绘制
        canvas.fill_circle_(grid, ONE, circle['x'], circle['y'], radius)


def brogue_designEntranceRoom(grid: array2d[int]):
    assert grid.width >= 22 and grid.height >= 12 
    
    grid.fill_(ZERO)
    
    room1_width = 8
    room1_height = 10
    room2_width = 20
    room2_height = 5
    room1_x = grid.width // 2 - room1_width // 2 - 1
    room1_y = grid.height - room1_height - 2
    room2_x = grid.width // 2 - room2_width // 2 - 1
    room2_y = grid.height - room2_height - 2

    canvas.fill_rect_(grid, ONE, room1_x, room1_y, room1_width, room1_height)
    canvas.fill_rect_(grid, ONE, room2_x, room2_y, room2_width, room2_height)
