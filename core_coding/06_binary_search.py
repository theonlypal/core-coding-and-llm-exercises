"""
Topic: Binary Search
Exercise: Search in Rotated Sorted Array (LeetCode 33)

Problem Description:
There is an integer array `nums` sorted in ascending order (with distinct values).

Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k` 
(1 <= k < nums.length) such that the resulting array is 
`[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (0-indexed). 
For example, `[0,1,2,4,5,6,7]` might be rotated at pivot index 3 and become `[4,5,6,7,0,1,2]`.

Given the array `nums` after the possible rotation and an integer `target`, 
return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Complexity Target:
Time: O(log N)
Space: O(1)
"""

def search_rotated(nums: list[int], target: int) -> int:
    """
    Searches for target in a rotated sorted array in O(log N) time.
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
            
        # Check if the left half is normally sorted
        if nums[left] <= nums[mid]:
            # Target is in the range of left sorted half
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Otherwise, the right half must be normally sorted
        else:
            # Target is in the range of right sorted half
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
                
    return -1

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Search in Rotated Sorted Array...")
    
    # Test case 1: target is present in right half
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    
    # Test case 2: target is not present
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    
    # Test case 3: array size 1
    assert search_rotated([1], 0) == -1
    
    # Test case 4: target is present in left half
    assert search_rotated([6, 7, 0, 1, 2, 4, 5], 7) == 1
    
    print("All tests passed successfully!")
