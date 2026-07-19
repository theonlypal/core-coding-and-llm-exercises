"""
Topic: Dynamic Programming (basic/intermediate)
Exercise: Coin Change (LeetCode 322)

Problem Description:
You are given an integer array `coins` representing coins of different denominations and 
an integer `amount` representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. 
If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Complexity Target:
Time: O(amount * len(coins))
Space: O(amount)
"""

def coin_change(coins: list[int], amount: int) -> int:
    """
    Computes the minimum number of coins needed to make up the amount using DP.
    """
    # DP array initialized to infinity (amount + 1 is a safe upper bound)
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed for 0 amount
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)
                
    return dp[amount] if dp[amount] != amount + 1 else -1

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Coin Change...")
    
    # Test case 1: Standard case
    assert coin_change([1, 2, 5], 11) == 3
    
    # Test case 2: Impossible combination
    assert coin_change([2], 3) == -1
    
    # Test case 3: Amount is 0
    assert coin_change([1], 0) == 0
    
    # Test case 4: Large amounts
    assert coin_change([1, 2, 5], 100) == 20
    
    print("All tests passed successfully!")
