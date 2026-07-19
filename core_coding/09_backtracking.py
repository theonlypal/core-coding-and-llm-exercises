"""
Topic: Backtracking
Exercise: Generate Parentheses (LeetCode 22)

Problem Description:
Given `n` pairs of parentheses, write a function to generate all combinations of 
well-formed parentheses.

Example 1:
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]

Complexity Target:
Time: O(4^n / sqrt(n)) - bounded by Catalan numbers.
Space: O(n) for recursion stack.
"""

def generate_parenthesis(n: int) -> list[str]:
    """
    Generates all combinations of well-formed parentheses using backtracking.
    """
    result = []
    
    def backtrack(current_str: str, open_count: int, close_count: int):
        # Base case: if the string length reaches 2 * n, we found a valid combination
        if len(current_str) == 2 * n:
            result.append(current_str)
            return
            
        # We can add an open parenthesis if we haven't used all n open parentheses
        if open_count < n:
            backtrack(current_str + "(", open_count + 1, close_count)
            
        # We can add a close parenthesis if there are more open parentheses than close parentheses
        if close_count < open_count:
            backtrack(current_str + ")", open_count, close_count + 1)
            
    backtrack("", 0, 0)
    return result

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Generate Parentheses...")
    
    # Test case 1: n = 1
    assert generate_parenthesis(1) == ["()"]
    
    # Test case 2: n = 3
    expected_3 = ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert sorted(generate_parenthesis(3)) == sorted(expected_3)
    
    # Test case 3: n = 2
    expected_2 = ["(())", "()()"]
    assert sorted(generate_parenthesis(2)) == sorted(expected_2)
    
    print("All tests passed successfully!")
