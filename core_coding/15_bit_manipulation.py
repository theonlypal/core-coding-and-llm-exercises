"""
Topic: Bit Manipulation
Exercise: Single Number (LeetCode 136) & Counting Bits (LeetCode 338)

Problem Description:
1. `single_number(nums)`: Every element in nums appears twice except for one. 
   Find that single element in O(N) time and O(1) space.
2. `count_bits(n)`: Given an integer n, return an array ans of length n + 1 
   where ans[i] is the number of 1's in the binary representation of i.

Example 1 (Single Number):
Input: nums = [4, 1, 2, 1, 2]
Output: 4

Example 2 (Counting Bits):
Input: n = 5
Output: [0, 1, 1, 2, 1, 2]
"""

from typing import List

def single_number(nums: List[int]) -> int:
    """
    Finds single number using XOR operation (a ^ a = 0, a ^ 0 = a).
    """
    result = 0
    for num in nums:
        result ^= num
    return result

def count_bits(n: int) -> List[int]:
    """
    Counts set bits for 0 to n in O(N) time using Bit DP.
    ans[i] = ans[i >> 1] + (i & 1)
    """
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Bit Manipulation...")
    
    # Single Number Tests
    assert single_number([2, 2, 1]) == 1
    assert single_number([4, 1, 2, 1, 2]) == 4
    assert single_number([1]) == 1
    
    # Counting Bits Tests
    assert count_bits(2) == [0, 1, 1]
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]
    
    print("All tests passed successfully!")
