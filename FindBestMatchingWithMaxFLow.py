from collections import deque

# =========================
# 基础：在残余网络中用 BFS 寻找增广路径
# =========================

def bfs_find_path(residual, s, t, parent):
    """
    在残余网络 residual 中用 BFS 寻找从 s 到 t 的一条“增广路径”。
    - residual[u][v] 表示 u->v 还能增加的剩余容量（>0 表示可走）
    - 找到路径后，用 parent 记录前驱：parent[v] = u
    - 返回 True 表示找到路径；False 表示不存在可增广路径
    """
    parent.clear()
    visited = set([s])
    q = deque([s])
    while q:
        u = q.popleft()
        for v, cap in residual[u].items():
            if cap > 0 and v not in visited:
                parent[v] = u
                if v == t:  # 提前结束：已到达汇点
                    return True
                visited.add(v)
                q.append(v)
    return False


# =========================
# Edmonds–Karp：最大流（用 BFS 找最短增广路）
# =========================

def edmonds_karp_max_flow(graph, s, t, show_steps=False):
    """
    计算从 s 到 t 的最大流。
    参数：
      - graph: dict-of-dict，graph[u][v] = 容量 c(u,v)
      - s: 源点
      - t: 汇点
      - show_steps: 是否打印每轮增广的路径与瓶颈
    返回：(max_flow, flow)
      - max_flow: 最大流数值
      - flow: 最终的“正向边实际流量”字典 flow[u][v]
    """
    # 1) 初始化残余网络（初始可用余量 = 原容量）
    residual = {u: dict(vs) for u, vs in graph.items()}
    # 确保所有潜在的反向边键存在（初值 0）
    for u in list(graph.keys()):
        for v in list(graph[u].keys()):
            if v not in residual:
                residual[v] = {}
            if u not in residual[v]:
                residual[v][u] = 0

    # 记录原图正向边的实际流量（仅用于输出展示）
    flow = {u: {v: 0 for v in graph[u]} for u in graph}

    max_flow = 0
    parent = {}
    round_id = 0

    while bfs_find_path(residual, s, t, parent):
        round_id += 1
        # 2) 回溯重建路径，并求瓶颈容量（路径上最小残余）
        path = []
        bottleneck = float('inf')
        v = t
        while v != s:
            u = parent[v]
            path.append((u, v))
            bottleneck = min(bottleneck, residual[u][v])
            v = u
        path.reverse()

        # 3) 沿路径增流，更新残余网络（正向减、反向加）
        for u, v in path:
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
            if u in graph and v in graph[u]:
                flow[u][v] += bottleneck
            else:
                # 若走的是残余图的反向边，则对应原图正向边撤回部分流量
                if v in flow and u in flow[v]:
                    flow[v][u] -= bottleneck

        max_flow += bottleneck

        if show_steps:
            path_str = " -> ".join([s] + [v for _, v in path])
            print(f"第 {round_id} 轮：增广路径 {path_str}，瓶颈 = {bottleneck}，当前总流 = {max_flow}")

    return max_flow, flow


# =========================
# 用最大流求二分图最大匹配
# =========================

def max_bipartite_matching_via_flow(left_nodes, right_nodes, edges, show_steps=True):
    """
    用最大流（Edmonds–Karp）求二分图最大匹配。
    输入：
      - left_nodes: 左侧点集合（例如候选人）
      - right_nodes: 右侧点集合（例如岗位）
      - edges: 允许匹配的边列表 [(u,v), ...]，其中 u∈left_nodes, v∈right_nodes
      - show_steps: 是否输出增广过程
    返回：
      - max_matching_size: 最大匹配的规模（匹配对数量）
      - matching_pairs: 具体匹配对列表 [(u,v), ...]
    做法（标准建模）：
      - 新增源点 s、汇点 t
      - s -> 每个左侧点 cap=1
      - 左侧点 u -> 右侧点 v cap=1（仅对允许的 (u,v)）
      - 每个右侧点 -> t cap=1
      - 求 s->t 的最大流；L->R 上 flow==1 的边即为匹配对
    """
    s, t = 's', 't'

    # 1) 初始化图节点
    graph = {s: {}, t: {}}
    for u in left_nodes:
        graph[u] = {}
    for v in right_nodes:
        graph[v] = {}

    # 2) s -> 左侧点（容量 1，保证每个左点最多匹配一次）
    for u in left_nodes:
        graph[s][u] = 1

    # 3) 左 -> 右（容量 1，表示一条潜在匹配关系）
    for (u, v) in edges:
        if u not in left_nodes or v not in right_nodes:
            raise ValueError(f"非法边 ({u},{v})：u 必须在左集，v 必须在右集")
        graph[u][v] = 1

    # 4) 右 -> t（容量 1，保证每个右点最多匹配一次）
    for v in right_nodes:
        graph[v][t] = 1

    # 5) 最大流
    max_flow, flow = edmonds_karp_max_flow(graph, s, t, show_steps=show_steps)

    # 6) 读取 L->R 上流量为 1 的边作为匹配结果
    matching_pairs = []
    for u in left_nodes:
        for v in right_nodes:
            if v in flow.get(u, {}) and flow[u][v] == 1:
                matching_pairs.append((u, v))

    return max_flow, matching_pairs


# =========================
# 演示：现实化的“候选人-岗位”最大匹配
# =========================
if __name__ == "__main__":
    # 左侧：候选人；右侧：岗位
    left = ['A1', 'A2', 'A3', 'A4']          # 4 位候选人
    right = ['J1', 'J2', 'J3', 'J4']         # 4 个岗位

    # 允许的匹配关系（谁能胜任哪个岗位）
    edges = [
        ('A1', 'J1'),
        ('A1', 'J2'),
        ('A2', 'J2'),
        ('A3', 'J2'),
        ('A3', 'J3'),
        ('A4', 'J1'),
        ('A4', 'J4'),
    ]

    print("\n================ 二分图最大匹配（用最大流） ================")
    size, pairs = max_bipartite_matching_via_flow(left, right, edges, show_steps=True)

    print("\n===== 匹配结果 =====")
    print(f"最大可匹配对数 = {size}")
    for u, v in pairs:
        print(f"  {u} -- {v}")

    # 说明：现在岗位有 4 个，上限就是 4；实际能否达到 4 取决于 edges 是否覆盖到 4 个不同岗位。