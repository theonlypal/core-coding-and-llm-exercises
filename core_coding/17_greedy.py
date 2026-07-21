"""
Topic: Greedy Algorithms
Exercise: Jump Game (LeetCode 55)

Problem Description:
You are given an integer array `nums`. You are initially positioned at the array's first index, 
and each element in the array represents your maximum jump length at that position.

Return `true` if you can reach the last index, or `false` otherwise.

Example 1:
Input: nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:
Input: nums = [3,2,1,0,4]
Output: false
Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, 
which makes it impossible to reach the last index.

Complexity Target:
Time: O(N)
Space: O(1)
"""

from typing import List

def can_jump(nums: List[int]) -> bool:
    """
    Determines if the last index can be reached using a greedy max-reachable approach.
    """
    max_reachable = 0
    target_idx = len(nums) - 1
    
    for i, jump_length in enumerate(nums):
        # If current index is beyond the maximum reachable index, we cannot proceed
        if i > max_reachable:
            return False
            
        max_reachable = max(max_reachable, i + jump_length)
        
        if max_reachable >= target_idx:
            return True
            
    return max_reachable >= target_idx

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Jump Game...")
    
    # Test case 1
    assert can_jump([2, 3, 1, 1, 4]) is True
    
    # Test case 2
    assert can_jump([3, 2, 1, 0, 4]) is False
    
    # Test case 3: Single element
    assert can_jump([0]) is True
    
    # Test case 4
    assert can_jump([2, 0, 0]) is True
    
    print("All tests passed successfully!")
