# -*- coding: utf-8 -*-
"""
序列比对（Sequence Alignment）——只使用 NumPy 的实现（全局比对 / Needleman–Wunsch 思想）
目标：对比两段英文句子（按“单词”为单位），找出最优对齐方式，并输出对齐结果与最终得分。

核心思路：
1) 动态规划 DP 表：dp[i, j] 表示“前 i 个单词的句子1”和“前 j 个单词的句子2”的最优对齐分数。
2) 转移：来自三种情况的最大值
   - 对角线（↘）：把 words1[i-1] 与 words2[j-1] 对齐（匹配或错配）
   - 上方（↑）：words1[i-1] 与 GAP 对齐（相当于句子2这边空一个）
   - 左方（←）：GAP 与 words2[j-1] 对齐（相当于句子1这边空一个）
3) 回溯：从右下角开始，根据 dp 的来源方向，反推出具体的对齐路径（即何处加 GAP）。

说明：
- 评分规则可以自由调整：match=+2, mismatch=-1, gap=-2（示例）
- 这里采用“全局对齐”（两边都要对齐到头和尾），适合长度接近、需要整体比对的场景。
"""

import numpy as np


def sequence_alignment_numpy(sentence1, sentence2):
    """
    功能：对两个英文句子做“按单词”的全局序列比对，并打印最优对齐与得分。
    参数：
        sentence1, sentence2: 字符串，英文句子。
    """
    # 1) 预处理：把句子按空格切分为“单词序列”（列表）
    words1 = sentence1.split()
    words2 = sentence2.split()

    # 两个序列的长度（m 表示句子1的单词数，n 表示句子2的单词数）
    m, n = len(words1), len(words2)

    # 2) 定义评分规则（可根据业务调整）
    match_score = 2       # 单词完全相同时的加分
    mismatch_score = -1   # 单词不同（错配）时的扣分
    gap_penalty = -2      # 引入空位 GAP（插入/删除）的惩罚

    # 3) 初始化 DP 表（(m+1) x (n+1)），类型为 int
    #    dp[i, j] 含义：句子1前 i 个单词 与 句子2前 j 个单词 的最优对齐分数
    dp = np.zeros((m + 1, n + 1), dtype=int)

    # 3.1) 初始化第一行：dp[0, j]
    #      含义：句子1为空串，与句子2前 j 个单词对齐 → 只能不断对句子2加 GAP 在句子1这边
    #      因此得分是 j 次 gap_penalty 的累加：0, -2, -4, ...
    dp[0, :] = np.arange(0, (n + 1) * gap_penalty, gap_penalty)

    # 3.2) 初始化第一列：dp[i, 0]
    #      含义：句子2为空串，与句子1前 i 个单词对齐 → 只能不断对句子1加 GAP
    dp[:, 0] = np.arange(0, (m + 1) * gap_penalty, gap_penalty)

    # 4) 填表（自顶向下，自左向右）
    #    对于每个 (i, j)，考虑三种转移来源：↘、↑、←，取最大值
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # 当前要对齐的两个单词（注意下标 -1）
            a = words1[i - 1]
            b = words2[j - 1]

            # 对角线情况（↘）：把 a 与 b 对齐
            #   若相同 → match_score；不同 → mismatch_score
            diag = dp[i - 1, j - 1] + (match_score if a == b else mismatch_score)

            # 上方情况（↑）：把 a 与 GAP 对齐（等价于在句子2这一侧插入一个空位）
            up = dp[i - 1, j] + gap_penalty

            # 左方情况（←）：把 GAP 与 b 对齐（等价于在句子1这一侧插入一个空位）
            left = dp[i, j - 1] + gap_penalty

            # 取三者中的最大值作为 dp[i, j]
            dp[i, j] = max(diag, up, left)

    # 5) 回溯（Traceback）：从右下角 (m, n) 出发，反向找出具体对齐路径
    aligned1, aligned2 = [], []   # 分别存放回溯构造出的“句子1对齐序列”和“句子2对齐序列”
    i, j = m, n

    # 只要还有任一序列未回溯完，就继续
    while i > 0 or j > 0:
        current = dp[i, j]  # 当前格子的最优得分

        # 情况A：来自对角线（↘）——把 words1[i-1] 与 words2[j-1] 对齐
        # 这里分“匹配”和“错配”两种计分，但来源判断都属于对角线
        if i > 0 and j > 0 and (
            (words1[i - 1] == words2[j - 1] and current == dp[i - 1, j - 1] + match_score)
            or (words1[i - 1] != words2[j - 1] and current == dp[i - 1, j - 1] + mismatch_score)
        ):
            aligned1.insert(0, words1[i - 1])  # 回溯是反向构造，所以用 insert(0, ...)
            aligned2.insert(0, words2[j - 1])
            i -= 1
            j -= 1

        # 情况B：来自上方（↑）——words1[i-1] 与 GAP 对齐（句子2“缺了一个”）
        elif i > 0 and current == dp[i - 1, j] + gap_penalty:
            aligned1.insert(0, words1[i - 1])
            aligned2.insert(0, "_")           # 这里用下划线 '_' 表示 GAP（空位）
            i -= 1

        # 情况C：来自左方（←）——GAP 与 words2[j-1] 对齐（句子1“缺了一个”）
        else:
            aligned1.insert(0, "_")
            aligned2.insert(0, words2[j - 1])
            j -= 1

    # 6) 打印结果（对齐后的两行与最终得分）
    print("\n=== Sequence Alignment Result ===")
    print("Sentence 1:", " ".join(aligned1))
    print("Sentence 2:", " ".join(aligned2))
    print("Final Alignment Score:", dp[m, n])

    # 可选：打印 DP 矩阵形状与内容，方便调试/学习
    print("\nDP matrix shape:", dp.shape)
    print(dp)


# === 演示入口 ===
if __name__ == "__main__":
    # 两段英文句子（你可以自由修改）
    s1 = "I love learning computer science every day"
    s2 = "I love to learn computer science everyday"

    # 调用主函数，执行序列比对并打印结果
    sequence_alignment_numpy(s1, s2)