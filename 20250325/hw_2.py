import requests
from bs4 import BeautifulSoup
import re  # 用於正則表達式匹配

def get_route_info(station_name):
    # 目標網站 URL
    url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"
    
    # 模擬瀏覽器的 HTTP 標頭
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # 設定編碼以正確解析中文
    if response.status_code != 200:
        print(f"無法連接到網站，狀態碼：{response.status_code}")
        return

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 鎖定「去程 (往松山車站)」下方的表格
    target_header = soup.find('td', string=re.compile(r'去程 \(往松山車站\)'))
    if not target_header:
        print("找不到去程標題")
        return

    # 找到最近的父表格容器
    table = target_header.find_next('table')
    
    # 提取所有車站名稱和到站時間
    station_data = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 2:  # 假設至少有兩欄：站名、到站時間
            station = cells[0].text.strip().replace('...', '')  # 去除末尾的省略符號
            arrival_time = cells[1].text.strip()  # 到站時間或狀態
            station_data.append((station, arrival_time))
    
    # 搜尋輸入的站名並顯示對應的到站時間
    found = False
    print(f"搜尋結果 - 站名: {station_name}")
    for station, arrival_time in station_data:
        if station_name in station:
            found = True
            if "未發車" in arrival_time:
                print(f"站名: {station}, 狀態: 尚未發車，時間: 無")
            elif "分" in arrival_time:
                print(f"站名: {station}, 狀態: 還有 {arrival_time} 到站，時間: {arrival_time}")
            elif "即將進站" in arrival_time:
                print(f"站名: {station}, 狀態: 即將進站，時間: 即將到達")
            else:
                print(f"站名: {station}, 狀態: {arrival_time}，時間: 無法解析")
    
    if not found:
        print(f"找不到 '{station_name}'，請檢查：")
        print("1. 是否包含『...』等省略符號")
        print("2. 是否完全符合站名（含全形括號）")
        print("3. 完整車站列表：")
        for station, _ in station_data:
            print(f"- {station}")

# 主程式
if __name__ == "__main__":
    station_name = input("請輸入去程站名: ").strip()
    get_route_info(station_name)