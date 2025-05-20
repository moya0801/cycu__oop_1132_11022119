import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# 指定 CSV 檔案的完整路徑
file_path = r"C:\Users\User\Documents\GitHub\cycu__oop_1132_11022119\20250520\midterm_scores.csv"

# 確保檔案存在
if not os.path.exists(file_path):
    print(f"錯誤：找不到檔案 '{file_path}'")
    exit()

# 讀取 CSV 檔案
try:
    data = pd.read_csv(file_path, encoding='utf-8-sig')
except Exception as e:
    print(f"錯誤：無法讀取檔案 '{file_path}'。詳細資訊：{e}")
    exit()

# 取得科目名稱
subjects = data.columns[2:]  # 從第3列開始為科目

# 設定分數區間
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
bin_labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]

# 計算每個科目在每個分數區間的人數
score_distribution = {subject: pd.cut(data[subject], bins=bins, labels=bin_labels).value_counts().sort_index() for subject in subjects}

# 繪製長條圖
x = np.arange(len(bin_labels))  # X 軸位置
width = 0.1  # 每個長條的寬度
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple']  # 紅橙黃綠藍靛紫

plt.figure(figsize=(12, 8))

for i, subject in enumerate(subjects):
    plt.bar(x + i * width, score_distribution[subject], width, label=subject, color=colors[i % len(colors)])

# 設定圖表標題和軸標籤
plt.title("成績分布圖", fontsize=16)  # 繁體中文標題
plt.xlabel("分數區間", fontsize=14)
plt.ylabel("人數", fontsize=14)
plt.xticks(x + width * (len(subjects) - 1) / 2, bin_labels, fontsize=12)  # 調整 X 軸刻度位置
plt.legend(loc='upper right', fontsize=12, title="科目", title_fontsize=14)  # 中文圖例

# 顯示圖表
plt.tight_layout()
plt.show()