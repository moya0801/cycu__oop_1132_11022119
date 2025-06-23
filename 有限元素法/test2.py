import numpy as np
import matplotlib.pyplot as plt

# 1. 節點座標 (手動輸入)
nodes = np.array([
    [0, 0],      # 0: 圓心
    [1, 0],      # 1: x軸正向
    [0, 1],      # 2: y軸正向
    [-1, 0],     # 3: x軸負向
    [0, -1]      # 4: y軸負向
])

# 2. 元素連接 (三角形)
elements = [
    [0, 1, 2],
    [0, 2, 3],
    [0, 3, 4],
    [0, 4, 1]
]

# 3. 元素剛性矩陣與載重向量
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

# 4. 組裝全域剛性矩陣與載重向量
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

# 5. 施加邊界條件 (圓周上的節點 u=0)
boundary_nodes = [1, 2, 3, 4]
for bn in boundary_nodes:
    K[bn, :] = 0
    K[bn, bn] = 1
    F[bn] = 0

# 6. 求解
U = np.linalg.solve(K, F)

# 7. 精確解
def exact_solution(x, y, Gtheta=5, a=1, b=1):
    return Gtheta * (a**2 * b**2) / (a**2 + b**2) * (1 - x**2 / a**2 - y**2 / b**2)

U_exact = np.array([exact_solution(x, y) for x, y in nodes])

# 8. 結果比較
print("Node |   FEM解   | 精確解")
for i, (ufem, uex) in enumerate(zip(U, U_exact)):
    print(f"{i:>4} | {ufem:8.4f} | {uex:8.4f}")

# 9. 節點解分布繪圖
plt.figure(figsize=(6,5))
plt.triplot(nodes[:,0], nodes[:,1], elements, color='gray', linestyle='--')
plt.tricontourf(nodes[:,0], nodes[:,1], elements, U, cmap='coolwarm', alpha=0.7)
for i, (x, y) in enumerate(nodes):
    plt.text(x, y, f"{U[i]:.2f}", color='k', fontsize=12, ha='center', va='center')
plt.colorbar(label='FEM u')
plt.title('FEM 節點解分布')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.show()