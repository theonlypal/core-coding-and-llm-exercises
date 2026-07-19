"""
Topic: Trees (DFS/BFS)
Exercise: Binary Tree Traversal (DFS: Max Depth, BFS: Level Order Traversal)

Problem Description:
Implement standard Depth-First Search (DFS) and Breadth-First Search (BFS) operations on a Binary Tree.
1. `max_depth`: Return the maximum depth/height of the binary tree (DFS).
2. `level_order_traversal`: Return the level order traversal of its nodes' values (BFS).

Example Tree:
       3
      / \
     9  20
       /  \
      15   7

1. Max Depth: 3
2. Level Order: [[3], [9, 20], [15, 7]]
"""

from collections import deque
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: Optional[TreeNode]) -> int:
    """
    Computes the maximum depth of a binary tree using DFS (recursive).
    """
    if not root:
        return 0
    
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    
    return max(left_depth, right_depth) + 1

def level_order_traversal(root: Optional[TreeNode]) -> list[list[int]]:
    """
    Computes the level order traversal of a binary tree using BFS (iterative with queue).
    """
    if not root:
        return []
        
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
        result.append(current_level)
        
    return result

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Binary Tree DFS/BFS...")
    
    # Constructing the tree:
    #      3
    #     / \
    #    9  20
    #      /  \
    #     15   7
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    
    # Verify DFS: max_depth
    depth = max_depth(root)
    assert depth == 3, f"Expected depth 3, got {depth}"
    
    # Verify BFS: level_order_traversal
    levels = level_order_traversal(root)
    expected_levels = [[3], [9, 20], [15, 7]]
    assert levels == expected_levels, f"Expected {expected_levels}, got {levels}"
    
    # Test with Empty Tree
    assert max_depth(None) == 0
    assert level_order_traversal(None) == []
    
    print("All tests passed successfully!")
