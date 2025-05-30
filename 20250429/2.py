import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib
from shapely.geometry import Point, LineString
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from datetime import datetime

# 設定中文字型（支援中文）
matplotlib.rcParams['font.family'] = 'Microsoft JhengHei'
matplotlib.rcParams['axes.unicode_minus'] = False

# 關閉互動模式
plt.ioff()

def read_route_csv(csv_path):
    """讀取路線的 CSV 檔案，並轉換為 GeoDataFrame"""
    df = pd.read_csv(csv_path, encoding='utf-8')
    geometry = [Point(lon, lat) for lon, lat in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf

def draw_multiple_routes_with_highlight(input_files: list, outputfile: str, highlight_station: str):
    """繪製多條路線，並在指定站名上新增高亮與進站中功能"""
    colors = ['blue', 'green', 'red', 'purple', 'orange']  # 預備多條線用不同顏色
    fig, ax = plt.subplots(figsize=(12, 12))

    station_found = False  # 紀錄是否找到站名

    # 載入背景圖片
    image_path = "20250429/1.jpg"
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"圖片檔案 {image_path} 不存在！")
    img = plt.imread(image_path)

    # 載入公車圖標
    bus_icon_path = r"C:\Users\User\Documents\GitHub\cycu__oop_1132_11022119\20250429\bus_icon_path.jpg"
    if not os.path.exists(bus_icon_path):
        raise FileNotFoundError(f"公車圖標檔案無法找到！請確認檔案是否存在於以下路徑：\n{bus_icon_path}")
    bus_img = plt.imread(bus_icon_path)

    for idx, file in enumerate(input_files):
        gdf = read_route_csv(file)
        color = colors[idx % len(colors)]

        # 繪製點
        gdf.plot(ax=ax, color=color, marker='o', markersize=5, label=f"路線 {os.path.basename(file)}")

        # 將點的 geometry 轉換為 LineString 並繪製線
        line_geometry = LineString(gdf.geometry.tolist())
        line_gdf = gpd.GeoDataFrame([1], geometry=[line_geometry], crs=gdf.crs)
        line_gdf.plot(ax=ax, color=color, linewidth=1)

        # 顯示每個站名
        for x, y, name, time_str in zip(gdf.geometry.x, gdf.geometry.y, gdf["車站名稱"], gdf["時間"]):
            ax.text(x, y, name, fontsize=6, ha='left', va='center')
            if name == highlight_station:
                # 特別標示輸入的站名，使用圖片替代點，並稍微偏移圖片位置
                imagebox = OffsetImage(img, zoom=0.05)  # 調整圖片大小
                ab = AnnotationBbox(imagebox, (x, y + 0.0005), frameon=False, zorder=5)  # 偏移圖片位置
                ax.add_artist(ab)
                station_found = True

            # 檢查時間是否在三分鐘以內
            current_time = datetime.now()
            station_time = datetime.strptime(time_str, "%H:%M:%S")
            if abs((current_time - station_time).total_seconds()) <= 180:
                # 新增公車圖標和「進站中」文字
                bus_imagebox = OffsetImage(bus_img, zoom=0.03)  # 調整公車圖標大小
                bus_ab = AnnotationBbox(bus_imagebox, (x, y - 0.0005), frameon=False, zorder=5)  # 偏移圖標位置
                ax.add_artist(bus_ab)
                ax.text(x, y - 0.001, "進站中", fontsize=8, color='red', ha='center', va='center')

    if not station_found:
        print(f"未找到站名: {highlight_station}")

    ax.set_title("多條公車路線圖")
    ax.set_xlabel("經度")
    ax.set_ylabel("緯度")
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    os.makedirs(os.path.dirname(outputfile), exist_ok=True)
    plt.savefig(outputfile, dpi=300)
    plt.close()

if __name__ == "__main__":
    input_files = [
        "20250429/bus_route_0161000900.csv",
        "20250429/bus_route_0161001500.csv"
    ]

    # 從終端機輸入站名
    highlight_station = input("請輸入要標示的站名: ")

    # 動態設定輸出檔案名稱，將車站名稱作為檔案名稱的一部分
    outputfile = f"20250429/{highlight_station}.png"

    draw_multiple_routes_with_highlight(input_files, outputfile, highlight_station)