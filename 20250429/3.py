import os

bus_icon_path = r"C:\Users\User\Documents\GitHub\cycu__oop_1132_11022119\20250429\bus_icon_path.jpg"
if os.path.exists(bus_icon_path):
    print("檔案存在，路徑正確！")
else:
    print(f"檔案不存在，請檢查路徑：{bus_icon_path}")