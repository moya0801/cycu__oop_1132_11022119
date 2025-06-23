import numpy as np

nodes = np.array([
    [0, 0],      # 0: center
    [1, 0],      # 1: right
    [0, 1],      # 2: top
    [-1, 0],     # 3: left
    [0, -1]      # 4: bottom
])

elements = [
    [0, 1, 2],
    [0, 2, 3],
    [0, 3, 4],
    [0, 4, 1]
]