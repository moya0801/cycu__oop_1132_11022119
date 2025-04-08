from datetime import datetime, timedelta

def calculate_julian_date(input_time: str) -> float:
    """
    計算輸入時間的儒略日 (Julian Date)。

    :param input_time: 使用者輸入的時間，格式為 'YYYY-MM-DD HH:MM:SS'
    :return: 對應的儒略日
    """
    # 將輸入時間轉換為 datetime 物件
    dt = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    
    # 計算儒略日
    julian_date = dt.toordinal() + 1721424.5 + (dt.hour + dt.minute / 60 + dt.second / 3600) / 24
    return julian_date

def calculate_days_since(input_time: str) -> float:
    """
    計算從輸入時間到現在的天數。

    :param input_time: 使用者輸入的時間，格式為 'YYYY-MM-DD HH:MM:SS'
    :return: 從輸入時間到現在的天數
    """
    # 將輸入時間轉換為 datetime 物件
    dt = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
    
    # 獲取現在時間
    now = datetime.now()
    
    # 計算時間差
    delta = now - dt
    return delta.total_seconds() / 86400  # 將秒數轉換為天數

if __name__ == "__main__":
    # 輸入時間
    input_time = input("請輸入時間 (格式: YYYY-MM-DD HH:MM:SS): ")
    
    try:
        # 計算儒略日
        julian_date = calculate_julian_date(input_time)
        print(f"輸入時間的儒略日 (Julian Date): {julian_date}")
        
        # 計算從輸入時間到現在的天數
        days_since = calculate_days_since(input_time)
        print(f"從輸入時間到現在的天數: {days_since:.2f}")
    except ValueError:
        print("輸入的時間格式不正確，請使用 'YYYY-MM-DD HH:MM:SS' 格式。")