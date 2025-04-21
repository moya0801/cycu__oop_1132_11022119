# -*- coding: utf-8 -*-
import requests
import csv
import os

def fetch_bus_data(routeid):
    # API URL
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={routeid}"
    
    try:
        # 發送 GET 請求
        response = requests.get(url)
        response.raise_for_status()  # 檢查請求是否成功
        
        # 檢查回應內容是否為 JSON
        try:
            data = response.json()  # 嘗試解析 JSON 資料
        except ValueError:
            print("回應內容不是有效的 JSON 格式，以下是回應內容：")
            print(response.text)  # 顯示回應的原始內容
            return

        # 提取站點資料
        stops = data.get("Stops", [])
        if not stops:
            print("未找到任何站點資料，請檢查公車代碼是否正確。")
            return

        parsed_data = []
        for stop in stops:
            arrival_info = stop.get("ArrivalTime", "未知")
            stop_number = stop.get("StopSequence", "未知")
            stop_name = stop.get("StopName", {}).get("Zh_tw", "未知")
            stop_id = stop.get("StopID", "未知")
            latitude = stop.get("StopPosition", {}).get("PositionLat", "未知")
            longitude = stop.get("StopPosition", {}).get("PositionLon", "未知")
            
            parsed_data.append([arrival_info, stop_number, stop_name, stop_id, latitude, longitude])

        # 確保資料夾存在
        os.makedirs("data", exist_ok=True)

        # 將資料寫入 CSV
        csv_filename = f"data/bus_route_{routeid}.csv"
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["arrival_info", "stop_number", "stop_name", "stop_id", "latitude", "longitude"])
            writer.writerows(parsed_data)

        print(f"資料已儲存至 {csv_filename}")

        # 顯示站點資訊
        for stop in parsed_data:
            print(f"到達時間: {stop[0]}, 車站序號: {stop[1]}, 車站名稱: {stop[2]}, 車站編號: {stop[3]}, 緯度: {stop[4]}, 經度: {stop[5]}")

    except requests.exceptions.RequestException as e:
        print(f"無法取得資料，請檢查網路連線或 API 是否有效：{e}")

if __name__ == "__main__":
    # 讓使用者輸入公車代碼
    routeid = input("請輸入公車代碼 (例如: 0100000200): ").strip()
    fetch_bus_data(routeid)