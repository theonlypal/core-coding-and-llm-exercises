"""
Topic: Matrix
Exercise: Spiral Matrix (LeetCode 54)

Problem Description:
Given an `m x n` `matrix`, return all elements of the `matrix` in spiral order.

Example 1:
Input: matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
]
Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]

Complexity Target:
Time: O(M * N) where M is rows and N is columns.
Space: O(1) extra space (excluding output array).
"""

from typing import List

def spiral_order(matrix: List[List[int]]) -> List[int]:
    """
    Returns all elements of the matrix in spiral order.
    """
    if not matrix or not matrix[0]:
        return []
        
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 1. Traverse Right (across top row)
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1
        
        # 2. Traverse Down (along right column)
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        
        # 3. Traverse Left (across bottom row)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
            
        # 4. Traverse Up (along left column)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
            
    return result

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Spiral Matrix...")
    
    # Test case 1
    m1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    assert spiral_order(m1) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    
    # Test case 2
    m2 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]
    assert spiral_order(m2) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    
    print("All tests passed successfully!")
