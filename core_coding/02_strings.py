"""
Topic: Strings
Exercise: Valid Palindrome (LeetCode 125)

Problem Description:
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters 
and removing all non-alphanumeric characters, it reads the same forward and backward. 
Alphanumeric characters include letters and numbers.

Given a string `s`, return `True` if it is a palindrome, or `False` otherwise.

Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Complexity Target:
Time: O(N) where N is the length of string s.
Space: O(1) extra space (using two pointers).
"""

def is_palindrome(s: str) -> bool:
    """
    Checks if a string is a palindrome using two pointers after filtering.
    """
    left, right = 0, len(s) - 1
    
    while left < right:
        # Move left pointer past non-alphanumeric characters
        while left < right and not s[left].isalnum():
            left += 1
        # Move right pointer past non-alphanumeric characters
        while left < right and not s[right].isalnum():
            right -= 1
            
        if s[left].lower() != s[right].lower():
            return False
            
        left += 1
        right -= 1
        
    return True

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Valid Palindrome...")
    
    # Test case 1: Standard palindrome with mixed casing/punctuation
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    
    # Test case 2: Not a palindrome
    assert is_palindrome("race a car") is False
    
    # Test case 3: Empty string (after filtering)
    assert is_palindrome(" ") is True
    
    # Test case 4: Single character
    assert is_palindrome("a") is True
    
    # Test case 5: Numeric characters
    assert is_palindrome("0P") is False
    
    print("All tests passed successfully!")
