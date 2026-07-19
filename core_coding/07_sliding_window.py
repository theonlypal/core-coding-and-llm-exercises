"""
Topic: Sliding Window
Exercise: Longest Substring Without Repeating Characters (LeetCode 3)

Problem Description:
Given a string `s`, find the length of the longest substring without repeating characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Complexity Target:
Time: O(N) where N is the length of string s.
Space: O(min(N, M)) where M is the character set size.
"""

def length_of_longest_substring(s: str) -> int:
    """
    Finds the length of the longest substring without repeating characters.
    """
    char_map = {}  # Map of character -> last index seen
    max_len = 0
    left = 0       # Left pointer of the sliding window
    
    for right, char in enumerate(s):
        # If the character is inside the current window, contract the window
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
            
        char_map[char] = right
        max_len = max(max_len, right - left + 1)
        
    return max_len

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Longest Substring Without Repeating Characters...")
    
    # Test case 1
    assert length_of_longest_substring("abcabcbb") == 3
    
    # Test case 2
    assert length_of_longest_substring("bbbbb") == 1
    
    # Test case 3
    assert length_of_longest_substring("pwwkew") == 3
    
    # Test case 4: Empty string
    assert length_of_longest_substring("") == 0
    
    # Test case 5: Unique characters
    assert length_of_longest_substring("abcdefg") == 7
    
    print("All tests passed successfully!")
