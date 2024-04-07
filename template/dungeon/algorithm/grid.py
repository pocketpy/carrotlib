from array2d import array2d
from collections import deque
import random

DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def find_connected_components(grid: array2d, value) -> tuple[array2d[int], int]:
    """获取图的所有连通分量
    
    返回`visited`数组与连通分量个数，其中`0`表示未访问，非`0`表示所在连通分量的索引（从1开始）
    """
    visited = array2d(grid.width, grid.height, default=0)
    queue = deque()
    count = 0       # 以连通分量的索引作为块的id
    for y in range(grid.height):
        for x in range(grid.width):
            if visited[x, y] or grid[x, y] != value:
                continue
            count += 1
            queue.append((x, y))
            visited[x, y] = count
            while queue:
                cx, cy = queue.popleft()
                for dx, dy in DIRS_4:
                    nx, ny = cx+dx, cy+dy
                    if grid.is_valid(nx, ny) and not visited[nx, ny] and grid[nx, ny] == value:
                        queue.append((nx, ny))
                        visited[nx, ny] = count
    return visited, count

def count_connected_components(grid: array2d, value) -> int:
    """计算图的连通分量个数"""
    _, count = find_connected_components(grid, value)
    return count

def find_largest_connected_component(grid: array2d, value) -> array2d[bool] | None:
    """获取图的面积最大的连通分量"""
    visited, count = find_connected_components(grid, value)
    if count == 0:
        return None
    counter = [0] * (count+1)
    for y in range(grid.height):
        for x in range(grid.width):
            counter[visited[x, y]] += 1
    counter[0] = 0  # 不考虑未访问的格子
    max_blob_id = counter.index(max(counter))
    return visited.map(lambda x: x == max_blob_id)

def iter_unordered(grid: array2d, cache: list = None) -> list[tuple[int, int]]:
    if not cache:
        for y in range(grid.height):
            for x in range(grid.width):
                cache.append((x,y))
    assert len(cache) == grid.numel
    random.shuffle(cache)
    return cache.copy()