"""
Topic: Two Pointers
Exercise: Two Sum II - Input Array Is Sorted (LeetCode 167)

Problem Description:
Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, 
find two numbers such that they add up to a specific `target` number. 

Return the indices of the two numbers, `index1` and `index2`, added by one as an integer array 
`[index1, index2]` of length 2.

The tests are generated such that there is exactly one solution. You may not use the same element twice.
Your solution must use only O(1) extra space.

Example 1:
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]

Complexity Target:
Time: O(N) where N is the length of numbers array.
Space: O(1) extra space.
"""

from typing import List

def two_sum_ii(numbers: List[int], target: int) -> List[int]:
    """
    Finds 1-indexed positions of two numbers adding to target using two pointers.
    """
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum < target:
            left += 1
        else:
            right -= 1
            
    return []

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Two Sum II...")
    
    # Test case 1
    assert two_sum_ii([2, 7, 11, 15], 9) == [1, 2]
    
    # Test case 2
    assert two_sum_ii([2, 3, 4], 6) == [1, 3]
    
    # Test case 3
    assert two_sum_ii([-1, 0], -1) == [1, 2]
    
    print("All tests passed successfully!")
