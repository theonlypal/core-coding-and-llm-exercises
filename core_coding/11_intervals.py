"""
Topic: Intervals
Exercise: Merge Intervals (LeetCode 56)

Problem Description:
Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping 
intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

Example 1:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Complexity Target:
Time: O(N log N) for sorting intervals.
Space: O(N) to store merged results.
"""

from typing import List

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merges overlapping intervals in O(N log N) time.
    """
    if not intervals:
        return []
        
    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        prev_start, prev_end = merged[-1]
        
        # Overlap detected
        if start <= prev_end:
            merged[-1][1] = max(prev_end, end)
        else:
            merged.append([start, end])
            
    return merged

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Merge Intervals...")
    
    # Test case 1
    input_1 = [[1, 3], [2, 6], [8, 10], [15, 18]]
    expected_1 = [[1, 6], [8, 10], [15, 18]]
    assert merge_intervals(input_1) == expected_1
    
    # Test case 2
    input_2 = [[1, 4], [4, 5]]
    expected_2 = [[1, 5]]
    assert merge_intervals(input_2) == expected_2
    
    # Test case 3: Unsorted input
    input_3 = [[6, 8], [1, 9]]
    expected_3 = [[1, 9]]
    assert merge_intervals(input_3) == expected_3
    
    print("All tests passed successfully!")
