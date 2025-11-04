from collections import deque
from copy import deepcopy

def bfs_find_path(residual, s, t, parent):
    """
    在残余网络 residual 中用 BFS 寻找从 s 到 t 的一条“增广路径”
    - residual[u][v] 表示 u->v 还能增加的剩余容量
    - 找到路径后，用 parent 记录每个点的前驱：parent[v] = u
    - 返回 True 表示找到，False 表示不存在
    """
    parent.clear()
    visited = set([s])
    q = deque([s])
    while q:
        u = q.popleft()
        for v, cap in residual[u].items():
            # 只走“还有剩余容量”的边，且不重复访问
            if cap > 0 and v not in visited:
                parent[v] = u
                if v == t:  # 一旦到达汇点，说明找到增广路径
                    return True
                visited.add(v)
                q.append(v)
    return False


def edmonds_karp_max_flow(graph, s, t, show_steps=True):
    """
    计算从 s 到 t 的最大流（Edmonds–Karp 实现）
    参数：
      - graph: 字典的字典，graph[u][v] = 容量
      - s: 源点
      - t: 汇点
      - show_steps: 是否打印每轮增广的详细过程
    返回：
      - max_flow: 最大流数值
      - flow: 最终的流量字典 flow[u][v] = 这条边被发送的流量
    思想：
      1) 用原图容量初始化残余网络 residual
      2) 不断用 BFS 在残余网络里找增广路径
      3) 计算该路径的瓶颈容量 Δ，沿路径增流；同时更新正/反向边的剩余容量
      4) 直到找不到增广路径为止
    """
    # 1) 残余网络：拷贝一份容量作为初始“可用余量”
    residual = {u: dict(vs) for u, vs in graph.items()}
    # 确保所有可能出现的反向边键存在（初始化为 0）
    for u in list(graph.keys()):
        for v in list(graph[u].keys()):
            if v not in residual:
                residual[v] = {}
            if u not in residual[v]:
                residual[v][u] = 0

    # 记录最终的“实际流量”flow（只在正向边上统计，便于阅读）
    flow = {u: {v: 0 for v in graph[u]} for u in graph}

    max_flow = 0
    parent = {}  # BFS 用来重建路径

    round_id = 0
    while bfs_find_path(residual, s, t, parent):
        round_id += 1
        # 2) 反向从 t 回溯到 s，找出路径的最小剩余容量（瓶颈）
        path = []
        bottleneck = float('inf')
        v = t
        while v != s:
            u = parent[v]
            path.append((u, v))
            bottleneck = min(bottleneck, residual[u][v])
            v = u
        path.reverse()  # 变成 s -> t 的顺序路径

        # 3) 沿路径增流，并更新残余网络（正向边减余量、反向边加余量）
        for u, v in path:
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
            # 如果这是原图的一条正向边，记录到 flow；否则是“借到”的反向边，不记正向表
            if u in graph and v in graph[u]:
                flow[u][v] += bottleneck
            else:
                # 走了残余图中的“反向边”，代表在原图里撤回一部分流
                # 对应正向边是 v->u
                if v in flow and u in flow[v]:
                    flow[v][u] -= bottleneck

        max_flow += bottleneck

        if show_steps:
            path_str = " -> ".join([s] + [v for _, v in path])
            print(f"第 {round_id} 轮：找到增广路径 {path_str}，瓶颈容量 = {bottleneck}，当前总流 = {max_flow}")
            # 可选：打印关键边的剩余容量
            # for u, v in path:
            #     print(f"  残余容量[{u}->{v}] = {residual[u][v]}，[{v}->{u}](反向) = {residual[v][u]}")

    return max_flow, flow


if __name__ == "__main__":
    # === 现实工程物流案例（北京→深圳，郑州/杭州/武汉中转）===
    # 含义：
    #   S=北京(源)，T=深圳(汇)
    #   A=郑州，B=杭州，C=武汉
    #   容量单位：吨/天
    logistics_graph = {
        'S': {'A': 20, 'B': 10},
        'A': {'C': 15},
        'B': {'C': 10},
        'C': {'T': 25},
        'T': {}
    }

    print("\n================ 现实工程物流案例 ================")
    max_flow, flow = edmonds_karp_max_flow(logistics_graph, 'S', 'T', show_steps=True)
    print("\n===== 结果总结 =====")
    print(f"最大流（北京→深圳的最大发电/发货能力） = {max_flow} 吨/天")
    print("各边实际流量（仅显示原图正向边）：")
    for u in logistics_graph:
        for v in logistics_graph[u]:
            print(f"  {u} -> {v} : {flow[u][v]}/{logistics_graph[u][v]}")