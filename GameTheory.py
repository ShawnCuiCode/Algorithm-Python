import nashpy as nash
import numpy as np

# 公司A、B的收益矩阵
A = np.array([
    [0, 1, -1],   # A出Rock，对应B出(Rock, Scissors, Paper)
    [-1, 0, 1],   # A出Scissors
    [1, -1, 0]    # A出Paper
])

# 玩家B的收益矩阵为A的相反数
B = -A

game = nash.Game(A, B)

print("📊 公司定价博弈（Prisoner's Dilemma 版本）")
print("公司A收益矩阵：\n", A)
print("公司B收益矩阵：\n", B)
print("-" * 40)

# 计算所有 Nash 均衡
for eq in game.support_enumeration():
    print("Nash 均衡：", eq)