import pandas as pd

def get_bus_info_go(bus_id):
    """
    根據 bus_id 回傳該路線的所有車站 ID (去程)

    Args:
        bus_id (str): 巴士的 ID

    Returns:
        list: 該路線的所有車站 ID (去程)
    """
    # 使用完整的檔案路徑
    csv_file = "C:/Users/User/Documents/GitHub/cycu__oop_1132_11022119/20250513/bus_route_0161000900.csv"

    try:
        # 讀取 CSV 檔案
        df = pd.read_csv(csv_file, encoding="utf-8")
        
        # 過濾出符合 bus_id 的資料
        filtered_rows = df[df["車站編號"].astype(str) == bus_id]
        
        # 如果找到資料，回傳所有車站 ID
        if not filtered_rows.empty:
            return df["車站編號"].tolist()
        else:
            return "該 bus_id 不存在於資料中"
    except FileNotFoundError:
        return "檔案不存在"
    except Exception as e:
        return f"處理檔案時發生錯誤: {e}"

# 測試函數
if __name__ == "__main__":
    bus_id = "1036300040"  # 替換為實際的 bus_id
    stop_ids = get_bus_info_go(bus_id)
    print(f"Stop IDs for Bus ID {bus_id}: {stop_ids}")