import pandas as pd
import os

# 指定 CSV 檔案的完整路徑
file_path = r"C:\Users\User\Documents\GitHub\cycu__oop_1132_11022119\20250520\midterm_scores.csv"

# 確保檔案存在並處理可能的編碼問題
if not os.path.exists(file_path):
    print(f"Error: The file '{file_path}' was not found.")
    exit()

try:
    # 嘗試以常見編碼讀取檔案
    data = pd.read_csv(file_path, encoding='utf-8-sig')
except UnicodeDecodeError:
    try:
        data = pd.read_csv(file_path, encoding='utf-8')
    except Exception as e:
        print(f"Error: Unable to read the file '{file_path}'. Details: {e}")
        exit()
except pd.errors.EmptyDataError:
    print(f"Error: The file '{file_path}' is empty or invalid.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()

# 設定不及格分數
fail_score = 60

# 計算每位學生不及格科目的數量
data['Fail_Count'] = (data.iloc[:, 2:] < fail_score).sum(axis=1)

# 找出每位學生的不及格科目名稱
subject_columns = data.columns[2:-1]  # 取得科目欄位名稱
data['Failed_Subjects'] = data.apply(
    lambda row: ', '.join(subject_columns[row[subject_columns] < fail_score]), axis=1
)

# 篩選出不及格科目數量超過一半的學生 (4科以上)
failed_students = data[data['Fail_Count'] >= 4]

# 選取需要的欄位 (名字、學生ID、不及格科目)
failed_students = failed_students[['Name', 'StudentID', 'Failed_Subjects']]

# 將結果輸出為 CSV 檔案
output_file = r"C:\Users\User\Documents\GitHub\cycu__oop_1132_11022119\20250520\failed_students.csv"
try:
    failed_students.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"不及格學生名單已輸出至 {output_file}")
except Exception as e:
    print(f"Error: Unable to write to the file '{output_file}'. Details: {e}")