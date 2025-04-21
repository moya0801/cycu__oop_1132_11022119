from datetime import datetime

def process_datetime(input_time):
    # 將輸入的時間字串轉換為 datetime 物件
    dt = datetime.strptime(input_time, "%Y-%m-%d %H:%M")
    
    # 1. 回傳該日期為星期幾
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[dt.weekday()]
    
    # 2. 回傳該日期是當年的第幾天
    day_of_year = dt.timetuple().tm_yday
    
    # 3. 計算從該時刻至現在共經過了幾個太陽日 (Julian date)
    now = datetime.now()
    julian_days = (now - dt).total_seconds() / 86400  # 1 太陽日 = 86400 秒
    
    # 回傳完整訊息
    return (
        f"輸入的時間為: {input_time}\n"
        f"該日期為: {weekday}\n"
        f"該日期是當年的第: {day_of_year} 天\n"
        f"從該時刻至現在共經過了: {julian_days:.6f} 太陽日"
    )

# 測試範例
if __name__ == "__main__":
    input_time = input("請輸入時間 (格式: YYYY-MM-DD HH:MM): ")
    result = process_datetime(input_time)
    print(result)