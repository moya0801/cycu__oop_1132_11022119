import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

def plot_log_normal_cdf(mu, sigma, output_file):
    """
    繪製對數常態累積分布函數 (CDF) 圖並儲存為圖片檔案。

    :param mu: 對數常態分佈的平均值
    :param sigma: 對數常態分佈的標準差
    :param output_file: 輸出的圖片檔案名稱
    """
    # 產生對數常態分佈的數據
    x = np.linspace(0.01, 10, 1000)  # 避免 log(0) 問題，x 從 0.01 開始
    cdf = lognorm.cdf(x, s=sigma, scale=np.exp(mu))  # 使用 scipy.stats.lognorm 計算 CDF

    # 繪製圖表
    plt.figure(figsize=(8, 6))
    plt.plot(x, cdf, label=f'μ={mu}, σ={sigma}')
    plt.title('Log-Normal Cumulative Distribution Function (CDF)')
    plt.xlabel('x')
    plt.ylabel('Cumulative Probability')
    plt.legend()
    plt.grid()

    # 儲存圖片
    plt.savefig(output_file)
    plt.close()

# 主程式
if __name__ == "__main__":
    mu = 1.5
    sigma = 0.4
    output_file = "log_normal_cdf.jpg"
    plot_log_normal_cdf(mu, sigma, output_file)
    print(f"累積分布函數圖已儲存為 {output_file}")