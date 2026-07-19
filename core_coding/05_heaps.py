"""
Topic: Heaps
Exercise: Kth Largest Element in an Array (LeetCode 215)

Problem Description:
Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array.
Note that it is the `k`th largest element in the sorted order, not the `k`th distinct element.

Can you solve it in O(N log k) time complexity and O(k) extra space?

Example 1:
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5

Complexity Target:
Time: O(N log K)
Space: O(K) to store the min-heap.
"""

import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Finds the Kth largest element using a min-heap of size K.
    """
    # Create a heap with the first k elements
    min_heap = nums[:k]
    heapq.heapify(min_heap)
    
    # Iterate through the rest of the elements
    for num in nums[k:]:
        if num > min_heap[0]:
            heapq.heappushpop(min_heap, num)
            
    # The root of the min-heap is the Kth largest element in nums
    return min_heap[0]

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Kth Largest Element...")
    
    # Test case 1
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    
    # Test case 2
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    
    # Test case 3: Array of size 1
    assert find_kth_largest([10], 1) == 10
    
    print("All tests passed successfully!")
