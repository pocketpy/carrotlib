# 测试用工具

from array2d import array2d

def print_grid_debug(*args, **kwargs):
    return
    print_grid(*args, **kwargs)
    input("Press Enter to continue...")

def print_grid(grid: array2d[int], message="------------------------", finish_walls=True):
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# Color Name	    Foreground Color Code	Background Color Code
# Black	            30	                    40
# Red	            31	                    41
# Green	            32	                    42
# Yellow	        33	                    43
# Blue	            34	                    44
# Magenta	        35	                    45
# Cyan	            36	                    46
# White	            37	                    47
# Default	        39	                    49
# Reset	            0	                    0
# Bright Black	    90	                    100
# Bright Red	    91	                    101
# Bright Green	    92	                    102
# Bright Yellow	    93	                    103
# Bright Blue	    94	                    104
# Bright Magenta	95	                    105
# Bright Cyan	    96	                    106
# Bright White	    97	                    107
    
    # (symbol, fg, bg)
    palette = {
        0: (".", 30, 0),
        1: ("1", 0, 41),
        2: ("2", 0, 42),
        3: ("3", 0, 43),
        6: ("6", 0, 35),
    }

    if finish_walls:
        grid = grid.copy()
        # 给grid进行描边，描边数值为6
        neighbors = grid.count_neighbors(1)
        for i in range(grid.width):
            for j in range(grid.height):
                if grid[i, j] == 0 and neighbors[i, j] > 0:
                    grid[i, j] = 6

    print(message)
    for y in range(grid.height):
        for x in range(grid.width):
            symbol, fg, bg = palette[grid[x, y]]
            symbol = symbol + ' '
            if fg == 0:
                print(f"\x1b[0;{bg}m{symbol}\x1b[0m", end="")
            else:
                print(f"\x1b[0;{fg}m{symbol}\x1b[0m", end="")
        print()
