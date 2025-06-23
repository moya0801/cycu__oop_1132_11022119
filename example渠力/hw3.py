import matplotlib.pyplot as plt

# 已知參數
b = 5         # 渠道寬度 (m)
Q = 5         # 流量 (m³/s)
n = 0.013     # Manning n
S0 = 0.001    # 坡度

def manning_eq(y):
    A = b * y
    P = b + 2 * y
    R = A / P
    Q_calc = (1/n) * A * (R ** (2/3)) * (S0 ** 0.5)
    return Q_calc

def f(y):
    return manning_eq(y) - Q

def df(y, delta=1e-6):
    return (f(y + delta) - f(y - delta)) / (2 * delta)

# 牛頓-拉弗森法
y_guess = 1.0
tolerance = 1e-6
max_iter = 100

for i in range(max_iter):
    y_new = y_guess - f(y_guess) / df(y_guess)
    if abs(y_new - y_guess) < tolerance:
        break
    y_guess = y_new

# 準備公式與計算過程
formula = (
    r"$Q = \dfrac{1}{n} A R^{2/3} S_0^{1/2}$" + "\n\n" +
    r"$A = b \times y$" + "\n" +
    r"$R = \dfrac{A}{P}$" + "\n" +
    r"$P = b + 2y$"
)

params = (
    r"已知參數：" + "\n" +
    rf"$b = {b}\ \mathrm{{m}}$" + "\n" +
    rf"$Q = {Q}\ \mathrm{{m^3/s}}$" + "\n" +
    rf"$n = {n}$" + "\n" +
    rf"$S_0 = {S0}$"
)

process = (
    r"牛頓-拉弗森法計算結果：" + "\n" +
    rf"$y = {y_new:.4f}\ \mathrm{{m}}$"
)

# 輸出成圖片
plt.figure(figsize=(10, 7))
plt.axis('off')
plt.text(0.05, 0.95, formula, fontsize=24, va='top')
plt.text(0.05, 0.60, params, fontsize=18, va='top')
plt.text(0.05, 0.40, process, fontsize=20, va='top', color='blue')
plt.savefig("normal_depth_result.jpg", bbox_inches='tight', dpi=200)
plt.show()