import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Node coordinates (center, right, top, left, bottom)
nodes = np.array([
    [0, 0],      # 0: center
    [1, 0],      # 1: right
    [0, 1],      # 2: top
    [-1, 0],     # 3: left
    [0, -1]      # 4: bottom
])

# 2. Element connectivity (four triangles)
elements = [
    [0, 1, 2],
    [0, 2, 3],
    [0, 3, 4],
    [0, 4, 1]
]

# 3. Element stiffness matrix and force vector
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

# 4. Assemble global stiffness matrix and force vector
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

# 5. Apply Dirichlet boundary conditions (u=0 on boundary nodes)
boundary_nodes = [1, 2, 3, 4]
for bn in boundary_nodes:
    K[bn, :] = 0
    K[bn, bn] = 1
    F[bn] = 0

# 6. Solve the linear system
U = np.linalg.solve(K, F)

# 7. Exact solution at nodes
def exact_solution(x, y, Gtheta=5, a=1, b=1):
    return Gtheta * (a**2 * b**2) / (a**2 + b**2) * (1 - x**2 / a**2 - y**2 / b**2)

U_exact = np.array([exact_solution(x, y) for x, y in nodes])

# 8. Output table (in English, with table name)
df = pd.DataFrame({
    "Node": np.arange(len(nodes)),
    "FEM": U,
    "Exact": U_exact
})
print("\nTable 1  Comparison of FEM and Exact Solution")
print(df.to_string(index=False))

# 9. Plot (dark lines, moderate markers, numbers offset, English caption below)
plt.figure(figsize=(6,5))
plt.triplot(nodes[:,0], nodes[:,1], elements, color='navy', linestyle='-', linewidth=1.8)
plt.tricontourf(nodes[:,0], nodes[:,1], elements, U, cmap='coolwarm', alpha=0.7)
plt.scatter(nodes[:,0], nodes[:,1], c='k', s=60, marker='o', edgecolors='w', zorder=12)

# Offset settings for node value labels (to avoid axis and overlap)
offsets = [
    (0.3, -0.3),   # center (move to lower right)
    (0.10, -0.08), # right
    (-0.08, 0.10), # top
    (-0.10, 0.08), # left
    (0.08, -0.10)  # bottom
]

for i, (x, y) in enumerate(nodes):
    dx, dy = offsets[i]
    plt.text(x+dx, y+dy, f"{U[i]:.2f}", color='k', fontsize=12, ha='center', va='center', zorder=20)

plt.colorbar(label='FEM u')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.tight_layout()
plt.subplots_adjust(bottom=0.18)
plt.figtext(0.5, 0.02, 'Figure 1  FEM Nodal Solution Distribution (4 Linear Triangular Elements)', ha='center', fontsize=13)
plt.show()