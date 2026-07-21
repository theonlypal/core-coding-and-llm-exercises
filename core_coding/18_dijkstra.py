"""
Topic: Graph Shortest Path (Dijkstra's Algorithm)
Exercise: Network Delay Time (LeetCode 743)

Problem Description:
You are given a network of `n` nodes, labeled from `1` to `n`. You are also given `times`, 
a list of travel times as directed edges `times[i] = (u_i, v_i, w_i)`, where `u_i` is the source node, 
`v_i` is the target node, and `w_i` is the time it takes for a signal to travel from source to target.

We will send a signal from a given node `k`. Return the minimum time it takes for all `n` nodes 
to receive the signal. If it is impossible for all `n` nodes to receive the signal, return `-1`.

Example 1:
Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2

Complexity Target:
Time: O((E + V) log V) where E is edges and V is vertices (n).
Space: O(V + E) for adjacency list and heap.
"""

import heapq
from collections import defaultdict
from typing import List

def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """
    Computes minimum time for signal to reach all nodes using Dijkstra's algorithm.
    """
    # 1. Build adjacency list: u -> list of (v, w)
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
        
    # 2. Min-heap stores tuples: (distance_so_far, current_node)
    min_heap = [(0, k)]
    
    # 3. Distance map: node -> shortest distance from k
    distances = {}
    
    while min_heap:
        d, node = heapq.heappop(min_heap)
        
        if node in distances:
            continue
            
        distances[node] = d
        
        # If all n nodes visited, we don't need to continue
        if len(distances) == n:
            break
            
        for neighbor, weight in graph[node]:
            if neighbor not in distances:
                heapq.heappush(min_heap, (d + weight, neighbor))
                
    # If not all nodes reached, return -1
    if len(distances) < n:
        return -1
        
    # Maximum distance among all nodes is the time signal takes to reach everywhere
    return max(distances.values())

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Network Delay Time (Dijkstra)...")
    
    # Test case 1
    t1 = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    assert network_delay_time(t1, n=4, k=2) == 2
    
    # Test case 2: Single node
    t2 = [[1, 2, 1]]
    assert network_delay_time(t2, n=2, k=1) == 1
    
    # Test case 3: Unreachable node
    t3 = [[1, 2, 1]]
    assert network_delay_time(t3, n=2, k=2) == -1
    
    print("All tests passed successfully!")
