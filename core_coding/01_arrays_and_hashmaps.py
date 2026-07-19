"""
Topic: Arrays & Hash Maps
Exercise: Group Anagrams (LeetCode 49)

Problem Description:
Given an array of strings `strs`, group the anagrams together.
You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a
different word or phrase, typically using all the original letters exactly once.

Example 1:
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Complexity Target:
Time: O(N * K log K) where N is the number of strings and K is the maximum length of a string.
Space: O(N * K) to store the grouped anagrams.
"""

from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Groups anagrams together using a hash map.
    """
    # Key: Sorted tuple of characters or sorted string
    # Value: List of anagrams matching that sorted key
    anagram_map = defaultdict(list)
    
    for s in strs:
        # Sorting the characters of the string to form the unique key
        sorted_key = "".join(sorted(s))
        anagram_map[sorted_key].append(s)
        
    return list(anagram_map.values())

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Group Anagrams...")
    
    # Test case 1
    input_1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
    output_1 = group_anagrams(input_1)
    # Sort sub-lists and outer list for comparison
    sorted_output_1 = sorted([sorted(group) for group in output_1])
    expected_1 = sorted([sorted(["bat"]), sorted(["nat", "tan"]), sorted(["ate", "eat", "tea"])])
    assert sorted_output_1 == expected_1, f"Expected {expected_1}, got {sorted_output_1}"
    
    # Test case 2
    input_2 = [""]
    output_2 = group_anagrams(input_2)
    assert output_2 == [[""]], f"Expected [['']], got {output_2}"
    
    # Test case 3
    input_3 = ["a"]
    output_3 = group_anagrams(input_3)
    assert output_3 == [["a"]], f"Expected [['a']], got {output_3}"
    
    print("All tests passed successfully!")
