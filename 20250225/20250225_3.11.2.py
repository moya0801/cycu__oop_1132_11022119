def print_right(text):
    # 計算需要的前導空格數量
    leading_spaces = 40 - len(text)
    # 打印帶有前導空格的字串
    print(' ' * leading_spaces + text)

# 測試範例
print_right("Monty")          # 輸出:                                    Monty
print_right("Python's")       # 輸出:                                Python's
print_right("Flying Circus")  # 輸出:                           Flying Circus
print_right("12345")          # 輸出:                                   12345
print_right("Hello, World!")  # 輸出:                           Hello, World!