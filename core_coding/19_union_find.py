"""
Topic: Union Find (Disjoint Set Union)
Exercise: Redundant Connection (LeetCode 684)

Problem Description:
In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with `n` nodes labeled from `1` to `n`, with one additional 
edge added. The added edge has two different vertices chosen from `1` to `n`, and was not an edge 
that already existed. The graph is represented as an array `edges` of length `n` where `edges[i] = [u_i, v_i]`.

Return an edge that can be removed so that the resulting graph is a tree of `n` nodes. 
If there are multiple answers, return the answer that appears last in the input.

Example 1:
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]

Complexity Target:
Time: O(N * alpha(N)) where alpha is the inverse Ackermann function (effectively O(N)).
Space: O(N) for parent array.
"""

from typing import List

class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size + 1))
        self.rank = [1] * (size + 1)
        
    def find(self, u: int) -> int:
        """
        Finds the representative root of u with path compression.
        """
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]
        
    def union(self, u: int, v: int) -> bool:
        """
        Unions two sets. Returns False if u and v are already in the same set (cycle detected).
        """
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u == root_v:
            return False  # Cycle detected!
            
        # Union by rank
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1
            
        return True

def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """
    Finds the redundant edge causing a cycle using Union-Find.
    """
    uf = UnionFind(len(edges))
    
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
            
    return []

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Union-Find (Redundant Connection)...")
    
    # Test case 1
    e1 = [[1, 2], [1, 3], [2, 3]]
    assert find_redundant_connection(e1) == [2, 3]
    
    # Test case 2
    e2 = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
    assert find_redundant_connection(e2) == [1, 4]
    
    print("All tests passed successfully!")
