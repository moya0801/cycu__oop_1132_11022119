import requests
from bs4 import BeautifulSoup
import re
import csv
import os

# 目標 URL
base_url = "https://ebus.gov.taipei/ebus"
route_detail_url = "https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
output_csv_file = "20250603/taipei_bus_routes_with_stops.csv"  # 定義輸出 CSV 檔案的名稱

# 確保輸出目錄存在
os.makedirs(os.path.dirname(output_csv_file), exist_ok=True)

def fetch_all_routes():
    """
    獲取所有公車路線的名稱與 ID。
    """
    print(f"正在從 {base_url} 獲取公車路線資訊...")
    response = requests.get(base_url)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有包含 'javascript:go()' 的 <a> 標籤
    links = soup.find_all('a', href=re.compile(r"javascript:go\('(.+)'\)"))
    routes = []
    for link in links:
        route_name = link.get_text().strip()
        match = re.search(r"go\('(.+)'\)", link['href'])
        if match:
            route_id = match.group(1)
            routes.append({'路線名稱': route_name, '路線ID': route_id})
    return routes

def fetch_route_stops(route_id):
    """
    獲取指定公車路線的車站資訊（去程與回程）。
    """
    print(f"正在獲取路線 ID {route_id} 的詳細車站資訊...")
    response = requests.get(route_detail_url.format(route_id=route_id))
    response.raise_for_status()
    data = response.json()

    stops = []
    for direction in ['GoBack', 'Back']:
        direction_name = "去程" if direction == 'GoBack' else "回程"
        for stop in data.get(direction, []):
            stops.append({
                '方向': direction_name,
                '站名': stop.get('StopName', {}).get('Zh_tw', '未知'),
                '站序': stop.get('StopSequence', '未知'),
                '站ID': stop.get('StopID', '未知'),
                '緯度': stop.get('StopPosition', {}).get('PositionLat', '未知'),
                '經度': stop.get('StopPosition', {}).get('PositionLon', '未知')
            })
    return stops

def main():
    try:
        # 獲取所有公車路線
        routes = fetch_all_routes()

        # 收集所有路線的詳細資訊
        all_data = []
        for route in routes:
            route_name = route['路線名稱']
            route_id = route['路線ID']
            stops = fetch_route_stops(route_id)
            for stop in stops:
                all_data.append({
                    '路線名稱': route_name,
                    '路線ID': route_id,
                    '方向': stop['方向'],
                    '站名': stop['站名'],
                    '站序': stop['站序'],
                    '站ID': stop['站ID'],
                    '緯度': stop['緯度'],
                    '經度': stop['經度']
                })

        # 將資料寫入 CSV
        print(f"\n正在將資料寫入 {output_csv_file}...")
        with open(output_csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['路線名稱', '路線ID', '方向', '站名', '站序', '站ID', '緯度', '經度']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)

        print(f"資料已成功寫入 {output_csv_file} 檔案。")

    except requests.exceptions.RequestException as e:
        print(f"獲取資料時發生錯誤: {e}")
    except Exception as e:
        print(f"處理資料時發生錯誤: {e}")

if __name__ == "__main__":
    main()