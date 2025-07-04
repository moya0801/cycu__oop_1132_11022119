import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Mesh generation: center + n_circle points
n_circle = 12  # 圓周分割數，元素數量也會是 n_circle
theta = np.linspace(0, 2*np.pi, n_circle+1)[:-1]
circle_nodes = np.stack([np.cos(theta), np.sin(theta)], axis=1)
nodes = np.vstack([[0,0], circle_nodes])  # 節點0為中心，其餘為圓周

# 2. Element connectivity
elements = []
for i in range(n_circle):
    n1 = 0
    n2 = i+1
    n3 = 1 if i+2 > n_circle else i+2
    elements.append([n1, n2, n3])

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
boundary_nodes = list(range(1, num_nodes))
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

# 8. Output table (show first 10 nodes)
df = pd.DataFrame({
    "Node": np.arange(len(nodes)),
    "FEM": U,
    "Exact": U_exact
})
print("\nTable 1  Comparison of FEM and Exact Solution (first 10 nodes)")
print(df.head(10).to_string(index=False))

# 9. Plot (dark lines, moderate markers, numbers offset, English caption below)
plt.figure(figsize=(6,6))
plt.triplot(nodes[:,0], nodes[:,1], elements, color='navy', linestyle='-', linewidth=1.2)
plt.tricontourf(nodes[:,0], nodes[:,1], elements, U, cmap='coolwarm', alpha=0.7)
plt.scatter(nodes[:,0], nodes[:,1], c='k', s=40, marker='o', edgecolors='w', zorder=12)

# Offset settings for node value labels (radially outward for circle nodes)
offsets = [(0.3, -0.3)]  # center
for i in range(n_circle):
    angle = theta[i]
    dx = 0.13 * np.cos(angle)
    dy = 0.13 * np.sin(angle)
    offsets.append((dx, dy))

for i, (x, y) in enumerate(nodes):
    dx, dy = offsets[i]
    plt.text(x+dx, y+dy, f"{U[i]:.2f}", color='k', fontsize=10, ha='center', va='center', zorder=20)

plt.colorbar(label='FEM u')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.tight_layout()
plt.subplots_adjust(bottom=0.18)
plt.figtext(0.5, 0.02, f'Figure 1  FEM Nodal Solution Distribution ({n_circle} Linear Triangular Elements)', ha='center', fontsize=13)
plt.show()