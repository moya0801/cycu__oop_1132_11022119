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

def element_stiffness_matrix(coords):
    x1, y1 = coords[0]
    x2, y2 = coords[1]
    x3, y3 = coords[2]
    area = 0.5 * abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))
    b = np.array([y2 - y3, y3 - y1, y1 - y2])
    c = np.array([x3 - x2, x1 - x3, x2 - x1])
    Ke = (1/(4*area)) * (np.outer(b, b) + np.outer(c, c))
    return Ke * area, area

def element_force_vector(area, Gtheta=5):
    f = 2 * Gtheta
    fe = f * area / 3 * np.ones(3)
    return fe

num_nodes = len(nodes)
K = np.zeros((num_nodes, num_nodes))
F = np.zeros(num_nodes)

for elem in elements:
    coords = nodes[elem]
    Ke, area = element_stiffness_matrix(coords)
    fe = element_force_vector(area)
    for i in range(3):
        for j in range(3):
            K[elem[i], elem[j]] += Ke[i, j]
        F[elem[i]] += fe[i]

boundary_nodes = [1, 2, 3, 4]
for bn in boundary_nodes:
    K[bn, :] = 0
    K[bn, bn] = 1
    F[bn] = 0

U = np.linalg.solve(K, F)

def exact_solution(x, y, Gtheta=5, a=1, b=1):
    return Gtheta * (a**2 * b**2) / (a**2 + b**2) * (1 - x**2 / a**2 - y**2 / b**2)

U_exact = np.array([exact_solution(x, y) for x, y in nodes])

print("Node |   FEM解   | 精確解")
for i, (ufem, uex) in enumerate(zip(U, U_exact)):
    print(f"{i:>4} | {ufem:8.4f} | {uex:8.4f}")

# 表格輸出
import pandas as pd
df = pd.DataFrame({
    "Node": np.arange(len(nodes)),
    "FEM解": U,
    "精確解": U_exact
})
print("\n表1  FEM與精確解比較表")
print(df.to_string(index=False))

# 繪圖
import matplotlib.pyplot as plt

plt.figure(figsize=(6,5))
plt.triplot(nodes[:,0], nodes[:,1], elements, color='navy', linestyle='-', linewidth=1.8)  # 深色線
plt.tricontourf(nodes[:,0], nodes[:,1], elements, U, cmap='coolwarm', alpha=0.7)
plt.scatter(nodes[:,0], nodes[:,1], c='k', s=60, marker='o', edgecolors='w', zorder=10)  # 適中大小標記
for i, (x, y) in enumerate(nodes):
    plt.text(x, y, f"{U[i]:.2f}", color='k', fontsize=12, ha='center', va='center', zorder=11)
plt.colorbar(label='FEM u')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.tight_layout()
plt.subplots_adjust(bottom=0.18)
plt.figtext(0.5, 0.02, '圖1  FEM 節點解分布 (四三角形線性元素)', ha='center', fontsize=13)  # 圖名在下
plt.show()