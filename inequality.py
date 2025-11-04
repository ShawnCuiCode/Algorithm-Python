import math

# ========== 参数 ==========
mu = 1        # 期望值 E[X]
a = 10        # 超过 10 个任务
sigma = 3     # 假设方差约为 3（举例用）
n = 1000      # 服务器总数
delta = (a - mu) / mu  # Chernoff 偏差比例

# ========== 各种不等式 ==========
# 1️⃣ Markov 不等式
markov = mu / a

# 2️⃣ Chebyshev 不等式
k = (a - mu) / sigma
chebyshev = 1 / (k ** 2)

# 3️⃣ Chernoff 上界（假设 X ~ Poisson 或二项分布）
chernoff = math.exp(-delta**2 * mu / 3)

# 4️⃣ Union Bound （系统中任一服务器超载）
union_bound = n * chernoff

# ========== 输出比较 ==========
print("📊 各不等式概率上界比较：\n")
print(f"Markov 上界:      P(X≥{a}) ≤ {markov:.4f}")
print(f"Chebyshev 上界:   P(X≥{a}) ≤ {chebyshev:.4f}")
print(f"Chernoff 上界:    P(X≥{a}) ≤ {chernoff:.3e}")
print(f"Union Bound 系统: P(any server overload) ≤ {union_bound:.3e}")