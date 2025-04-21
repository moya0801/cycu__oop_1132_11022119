import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_normal_pdf(mu, sigma):
    # 建立 x 軸範圍
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    # 計算常態分佈的 PDF
    y = norm.pdf(x, mu, sigma)
    
    # 繪製圖形
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'μ={mu}, σ={sigma}')
    plt.title('Normal Distribution PDF')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.grid(True)
    
    # 儲存圖形為 JPG
    plt.savefig('normal_pdf.jpg')
    plt.close()

# 測試範例
if __name__ == "__main__":
    plot_normal_pdf(0, 1)  # μ=0, σ=1