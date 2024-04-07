from array2d import array2d
import random

from dungeon.brogue.const import *
from dungeon.algorithm.grid import find_largest_connected_component

'''
cavern.py 集合了所有关于生成特定洞穴房间的算法
'''

# ---------------------------------洞穴---------------------------------
# 关于洞穴的生成算法, 程序将不断尝试在max_width, max_height内随机生成块, 而直到块的规格符合要求时才会停止
# 根据经验, 它们的规格多数集中在max_width/2, max_height/2附近, 因此当块的下限min_width, min_height大于max_width/2, max_height/2时, 将很难在短时间内生成洞穴
# 因此对于下列预设的函数, 传入的grid的规格需要尽可能大(我已经基于大量测试设定了合适的assert限制), 以防止生成速度变慢, 甚至是超出1000次的重新生成限制报AssertionError

def brogue_design_compat_cavern(grid: array2d):
    _brogue_designCavern(grid, 3, 12, 4, 8)

def brogue_design_large_north_south_cavern(grid: array2d):
    assert grid.width >= 4 and grid.height >= 18
    _brogue_designCavern(grid, 3, 12, 15, grid.height-2)

def brogue_design_large_east_west_cavern(grid: array2d):
    assert grid.width >= 22 and grid.height >= 22
    _brogue_designCavern(grid, 20, grid.height-2, 4, 8)

def brogue_design_cave(grid: array2d):
    assert grid.width >= CAVE_MIN_WIDTH and grid.height >= CAVE_MIN_HEIGHT
    _brogue_designCavern(grid, CAVE_MIN_WIDTH, grid.width-2, CAVE_MIN_HEIGHT, grid.height-2)



# ----------- _brogue_designCavern 为原作函数, 以上为原作中调用该函数的四个地方
def _brogue_designCavern(grid: array2d[int], min_width: int, max_width: int, min_height: int, max_height: int):
    """
    使用元胞自动机生成限定规格的一块洞穴样式的房间
    """
    assert min_width <= max_width and min_height <= max_height
    
    grid.fill_(ZERO)
    
    blob_grid = array2d(max_width, max_height, default=None)  # 用来培育块的网格, 尺寸为块的最大尺寸
    round_count = 2  # 当它被设定地很高时, 生成将非常耗时, 当它越大, 房间越大,但是边缘越粗糙, 反之, 当它越小,房间越小,边缘越光滑
    noise_probability = 0.55
    birth_parameters = "ffffffttt"
    survival_parameters = "ffffttttt"
    blob_grid = _brogue_createBlobOnGrid(blob_grid, min_width, max_width, min_height, max_height, round_count, noise_probability, birth_parameters, survival_parameters)
    
    # 下面将生成的块从blob_grid中复制到grid中
    blob_w, blob_h = blob_grid.width, blob_grid.height

    # 把blob_grid复制到grid的中心
    grid_x = (grid.width - blob_w) // 2
    grid_y = (grid.height - blob_h) // 2
    grid[grid_x: grid_x+blob_w, grid_y: grid_y+blob_h] = blob_grid



# _brogue_designCavern 的一部分, 用于构造房间, _brogue_designCavern会将该房间插入到大的grid
def _brogue_createBlobOnGrid(
    grid: array2d[int], 
    blob_min_width: int, 
    blob_max_width: int, 
    blob_min_height: int,  
    blob_max_height: int,  
    round_count = 5, 
    noise_probability = 0.55, 
    birth_parameters = 'ffffffttt',  
    survival_parameters = 'ffffttttt' \
    ) -> array2d[int]:
    '''
    本函数利用细胞自动机按照培育参数在给定的空网格之内生成图案, 并返回最大的块在网格中的位置和规格
    
    参数列表:
        grid:  
            用于培育块的网格
        blob_min_width:  
            用于限制块的规格
        blob_max_width:  
            用于限制块的规格
        blob_min_height:  
            用于限制块的规格
        blob_max_height:   
            用于限制块的规格
        round_count = 10:  
            细胞自动机的迭代次数
        noise_probability = 0.55 :
            初始噪声的生成率 
        birth_parameters = 'ffffffttt' :
            长度为9的字符串, 表示当前格子附近3x3区域内存在index个细胞时, birth_parameters[index]的值(t/f)将决定本格子是否在下一轮迭代时生成细胞, 或使本格子细胞存活
        survival_parameters = 'ffffttttt' :
            同上, 假如本格子不会诞生新细胞, 那么这个参数将判定周围细胞的密度以决定下一轮迭代时本格子的细胞是否会被销毁, 't'表示存活, 'f'表示销毁
    
    返回值:
        四元组, 其中每个元素分别表示最大块外接矩形的 (左上角x坐标, 左上角y坐标, 宽度, 高度)
    '''
    
    survival_value, dead_value = -1, -2
    TIME_OUT_LOOP = 2000
    loop_count = 0
    while True:
        loop_count += 1
        assert loop_count <= TIME_OUT_LOOP
        
        # ---- 生成初始噪声
        grid.apply_(lambda _: survival_value if random.random() < noise_probability else dead_value)
        
        # ---- 细胞自动机开始数轮迭代
        for _ in range(round_count):
            # 每轮迭代遍历并修改 blob_grid 所有格子
            last_grid = grid.copy()  # 记录上一轮迭代的最终结果, 接下来将就地修改blob_grid

            # 计算当前格子的周围中存在活细胞的数量
            live_neighbors = grid.count_neighbors(survival_value)
            
            for cell_x in range(grid.width):
                for cell_y in range(grid.height):
                    # 计算本轮迭代中该格子的细胞的命运
                    nb_count = live_neighbors[cell_x, cell_y]
                    last_value = last_grid[cell_x, cell_y]
                    # 原作实现：
                    # if (!buffer2[i][j] && birthParameters[nbCount] == 't') {
                    #     grid[i][j] = 1; // birth
                    # } else if (buffer2[i][j] && survivalParameters[nbCount] == 't') {
                    #     // survival
                    # } else {
                    #     grid[i][j] = 0; // death
                    # }
                    if last_value == dead_value and birth_parameters[nb_count] == 't':
                        grid[cell_x, cell_y] = survival_value   # birth
                    elif last_value == survival_value and survival_parameters[nb_count] == 't':
                        pass    # survival
                    else:
                        grid[cell_x, cell_y] = dead_value
        
        largest = find_largest_connected_component(grid, survival_value)
        if largest is not None:
            blob_x, blob_y, blob_w, blob_h = largest.find_bounding_rect(True)
            # 检测是否满足对块的规格限制
            if (blob_min_width <= blob_w <= blob_max_width) and (blob_min_height <= blob_h <= blob_max_height):
                largest = largest[blob_x: blob_x+blob_w, blob_y: blob_y+blob_h]
                return largest.map(lambda x: ONE if x else ZERO)
