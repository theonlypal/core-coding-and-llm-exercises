"""
Topic: Graphs
Exercise: Number of Islands (LeetCode 200)

Problem Description:
Given an `m x n` 2D binary grid `grid` which represents a map of '1's (land) and '0's (water), 
return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. 
You may assume all four edges of the grid are all surrounded by water.

Example 1:
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Complexity Target:
Time: O(M * N) where M is rows and N is columns.
Space: O(M * N) in the worst case (stack space due to recursion/DFS).
"""

def num_islands(grid: list[list[str]]) -> int:
    """
    Counts the number of islands in a grid using DFS.
    """
    if not grid or not grid[0]:
        return 0
        
    rows, cols = len(grid), len(grid[0])
    island_count = 0
    
    def dfs(r: int, c: int):
        # Base cases: out of bounds or water ('0')
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
            
        # Mark as visited by sinking the land
        grid[r][c] = '0'
        
        # Traverse in 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                island_count += 1
                dfs(r, c)
                
    return island_count

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Number of Islands...")
    
    # Test case 1
    grid_1 = [
      ["1","1","1","1","0"],
      ["1","1","0","1","0"],
      ["1","1","0","0","0"],
      ["0","0","0","0","0"]
    ]
    assert num_islands(grid_1) == 1
    
    # Test case 2
    grid_2 = [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
    assert num_islands(grid_2) == 3
    
    # Test case 3: Empty grid
    assert num_islands([]) == 0
    
    print("All tests passed successfully!")
