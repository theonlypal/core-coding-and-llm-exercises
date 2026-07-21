"""
Topic: Monotonic Stack
Exercise: Daily Temperatures (LeetCode 739)

Problem Description:
Given an array of integers `temperatures` represents the daily temperatures, 
return an array `answer` such that `answer[i]` is the number of days you have to wait 
after the `i`-th day to get a warmer temperature. 

If there is no future day for which this is possible, keep `answer[i] == 0` instead.

Example 1:
Input: temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
Output: [1, 1, 4, 2, 1, 1, 0, 0]

Complexity Target:
Time: O(N) where N is the length of temperatures array.
Space: O(N) for the stack.
"""

from typing import List

def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    Finds days to wait for a warmer temperature using a monotonic decreasing stack.
    """
    n = len(temperatures)
    answer = [0] * n
    stack = []  # Stores indices of temperatures in decreasing order of temperature value
    
    for i, temp in enumerate(temperatures):
        # Pop colder temperatures from stack and calculate days waited
        while stack and temp > temperatures[stack[-1]]:
            prev_day_idx = stack.pop()
            answer[prev_day_idx] = i - prev_day_idx
            
        stack.append(i)
        
    return answer

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Daily Temperatures...")
    
    # Test case 1
    input_1 = [73, 74, 75, 71, 69, 72, 76, 73]
    expected_1 = [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures(input_1) == expected_1
    
    # Test case 2
    input_2 = [30, 40, 50, 60]
    expected_2 = [1, 1, 1, 0]
    assert daily_temperatures(input_2) == expected_2
    
    # Test case 3
    input_3 = [30, 60, 90]
    expected_3 = [1, 1, 0]
    assert daily_temperatures(input_3) == expected_3
    
    print("All tests passed successfully!")
