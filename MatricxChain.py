def matrix_chain_order(p):
    """
    p: list of matrix dimensions, e.g. [10, 100, 5, 50, 1]
    Means M1:10x100, M2:100x5, M3:5x50, M4:50x1
    """
    n = len(p) - 1
    # m[i][j] stores the minimum multiplication cost from i to j
    m = [[0 for _ in range(n)] for _ in range(n)]

    # chain_len: how many matrices are being multiplied
    for chain_len in range(2, n + 1):
        for i in range(n - chain_len + 1):
            j = i + chain_len - 1
            m[i][j] = float('inf')

            for k in range(i, j):
                # cost = left part + right part + combine cost
                cost = m[i][k] + m[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if cost < m[i][j]:
                    m[i][j] = cost  # keep the smallest one

    return m[0][n - 1]


# === Run demo ===
if __name__ == '__main__':
    p = [10, 100, 5, 50, 1]
    print("Minimum cost:", matrix_chain_order(p))