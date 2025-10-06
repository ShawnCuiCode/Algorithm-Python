# 案例：开一家奶茶店
# 你是一家奶茶店老板，要制作三种饮品：
#
# 🍓 奶昔（N1）
#
# 🍫 巧克力奶茶（N2）
#
# 🍋 柠檬绿茶（N3）
#
# 每种饮品都需要不同的原材料，比如：
#
# R1：牛奶
#
# R2：糖
#
# R3：茶叶
#
# 你每天只进货固定量的原材料，比如：
#
# 牛奶：10升
#
# 糖：8公斤
#
# 茶叶：6包

import numpy as np, time

def solve_milk_tea_problem():
    A = np.array([[2, 1, 0],
                  [1, 2, 1],
                  [0, 1, 2]])

    b = np.array([10, 1, 2])

    x = np.linalg.solve(A, b)
    print(f"奶昔：{x[0]:.0f} 杯，巧克力奶茶：{x[1]:.0f} 杯，柠檬绿茶：{x[2]:.0f} 杯")


import pandas as pd
import matplotlib.pyplot as plt



def analyze_sales():
    # Step 1: Create sales data
    data = {
        'Date': ['2025-10-01', '2025-10-02', '2025-10-03'],
        'Milkshake': [20, 25, 22],
        'ChocolateMilkTea': [15, 18, 20],
        'LemonGreenTea': [10, 12, 15]
    }
    df = pd.DataFrame(data)

    # Step 2: Convert date strings to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])

    # Step 3: Calculate total daily sales
    df['TotalSales'] = df[['Milkshake', 'ChocolateMilkTea', 'LemonGreenTea']].sum(axis=1)

    # Step 4: Print summary
    print("Daily Sales Summary:")
    print(df)

    # Step 5: Plot total sales trend
    plt.figure(figsize=(8, 5))
    plt.plot(df['Date'], df['TotalSales'], marker='o', label='Total Sales')
    plt.title('Daily Total Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Cups Sold')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def range_test():
    a = list(range(1000000))
    b = np.array(a)

    # list
    start = time.time()
    c = [x * 2 for x in a]
    print("list time:", time.time() - start)

    # numpy
    start = time.time()
    d = b * 2
    print("numpy time:", time.time() - start)

# Run the main function
if __name__ == "__main__":
    # analyze_sales()
    # solve_milk_tea_problem()
    # print(pd.__version__)
    # print(np.__version__)
    range_test()



