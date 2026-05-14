import numpy as np
import csv

input_file = 'Grocery_Inventory_and_Sales_Dataset.csv'
output_file = 'Grocery_Inventory_Calculated.csv'

# 1. 讀取資料
with open(input_file, mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = list(reader)

# 2. 萃取欄位並轉換為 NumPy 陣列
product_names = np.array([row[1] for row in data])
stock_quantities = np.array([row[5] for row in data], dtype=float)
sales_volumes = np.array([row[13] for row in data], dtype=float)

# 清理 'Unit_Price'：移除 '$'，並轉換為 float 的 NumPy 陣列
unit_prices = np.array([row[8].replace('$', '').replace(',', '') for row in data], dtype=float)

# ==========================================
# 核心計算 (NumPy)
# ==========================================

# (1) 計算每個商品的總庫存價值
total_inventory_values = stock_quantities * unit_prices

# (2) 找出最暢銷的商品
best_selling_idx = np.argmax(sales_volumes)
best_selling_product = product_names[best_selling_idx]
best_selling_volume = sales_volumes[best_selling_idx]

# (3) 計算 9 折後的總收入
total_revenues = sales_volumes * unit_prices
discounted_revenues = total_revenues * 0.9
total_discounted_revenue = np.sum(discounted_revenues)

# ==========================================
# 匯出新 CSV 檔案
# ==========================================

new_header = header + ['Unit_Price_Float', 'Total_Inventory_Value', 'Total_Revenue', 'Discounted_Revenue']

with open(output_file, mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(new_header)

    for i in range(len(data)):
        row_data = data[i] + [
            f"{unit_prices[i]:.2f}",
            f"{total_inventory_values[i]:.2f}",
            f"{total_revenues[i]:.2f}",
            f"{discounted_revenues[i]:.2f}"
        ]
        writer.writerow(row_data)

# 印出結果供報告使用
print("=== 執行結果 ===")
print(f"(2) 最暢銷商品: {best_selling_product} (銷售量: {int(best_selling_volume)})")
print(f"(3) 9折後全店總收入: ${total_discounted_revenue:,.2f}")