import numpy as np

def delay1(f): return 3 * f
def delay2(f): return 5
def total_cost(f1):
    f2 = 1 - f1
    return f1 * delay1(f1) + f2 * delay2(f2)

f_values = np.linspace(0, 1, 21)
costs = [total_cost(f) for f in f_values]

f1_opt = f_values[np.argmin(costs)]
print("✅ 社会最优 f1 =", f1_opt, "f2 =", 1 - f1_opt, "最小总延迟 =", min(costs))