import heapq
from collections import defaultdict

def pretty_dist(dist, fixed):
    """
    Conversational: Make a compact, readable snapshot of current best-known distances.
    'fixed' are nodes whose shortest path is finalized.
    """
    items = []
    for k in sorted(dist.keys()):
        val = "∞" if dist[k] == float('inf') else str(dist[k])
        flag = "*" if k in fixed else " "
        items.append(f"{k}:{val}{flag}")
    return " | ".join(items)

def dijkstra(graph, source, verbose=False):
    """
    graph: dict[node] -> list[(neighbor, weight)]
    source: start node
    verbose: if True, print step-by-step logs

    Returns:
      dist: dict of shortest distances from source to each node
      prev: dict of predecessors to reconstruct shortest paths
    """
    # Best-known distances; start at 0 for source and +∞ for others
    dist = {v: float('inf') for v in graph}
    dist[source] = 0

    # To reconstruct actual shortest paths
    prev = {v: None for v in graph}

    # Min-heap priority queue of (distance, node)
    pq = [(0, source)]
    fixed = set()  # nodes whose shortest path is finalized

    step = 0
    if verbose:
        print("=== Dijkstra step-by-step ===")
        print(f"Initial distances: {pretty_dist(dist, fixed)}")
        print(f"Initial heap: {pq}\n")

    while pq:
        cur_d, u = heapq.heappop(pq)

        if u in fixed:
            if verbose:
                print(f"[Skip] Pop ({cur_d}, {u}) but {u} is already finalized.\n")
            continue

        # Finalize u's shortest distance
        fixed.add(u)

        if verbose:
            step += 1
            print(f"Step {step}: pop ({cur_d}, {u})  -> finalize {u}")
            print(f"Distances before relaxing neighbors of {u}:")
            print(f"  {pretty_dist(dist, fixed)}")

        # Relax outgoing edges u -> v
        for v, w in graph[u]:
            if v in fixed:
                # No need to update finalized nodes
                continue

            # If going through u gives a shorter path to v, update it
            if dist[v] > dist[u] + w:
                old = dist[v]
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
                if verbose:
                    old_str = "∞" if old == float('inf') else str(old)
                    print(f"  Relax ({u} -> {v}, w={w}): "
                          f"dist[{v}] {old_str} -> {dist[v]}   (prev[{v}]={u})")
            else:
                if verbose:
                    cur_best = "∞" if dist[v] == float('inf') else str(dist[v])
                    print(f"  Keep  ({u} -> {v}, w={w}): "
                          f"dist[{v}] stays {cur_best}")

        if verbose:
            print(f"Heap now: {pq}")
            print(f"Distances after relaxing {u}:")
            print(f"  {pretty_dist(dist, fixed)}\n")

    if verbose:
        print("=== Done ===\n")
    return dist, prev

def reconstruct_path(prev, target):
    """
    Conversational: Walk backwards from the target to rebuild the actual shortest route.
    """
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path

if __name__ == "__main__":
    # Conversational: Build the same undirected weighted "city map" we used in the story.
    # Roads (undirected):
    # A-B(3), A-D(4), A-E(7), B-C(10), B-D(4), D-C(8), D-E(8), E-C(2)
    edges = [
        ("A", "B", 3),
        ("A", "D", 4),
        ("A", "E", 7),
        ("B", "C", 10),
        ("B", "D", 4),
        ("D", "C", 8),
        ("D", "E", 8),
        ("E", "C", 2),
    ]

    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))  # undirected

    source = "A"
    # Turn on verbose to see step-by-step logs
    dist, prev = dijkstra(graph, source, verbose=True)

    # Print final results
    print("=== Final shortest distances and routes ===")
    print(f"Source: {source}")
    for node in sorted(graph.keys()):
        if node == source:
            continue
        route = reconstruct_path(prev, node)
        if dist[node] == float('inf'):
            print(f"Destination: {node:>2} | No reachable path")
        else:
            print(f"Destination: {node:>2} | Distance: {dist[node]:>2} | Path: {' -> '.join(route)}")