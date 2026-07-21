"""
Topic: Trie / Prefix Tree
Exercise: Implement Trie (Prefix Tree) (LeetCode 208)

Problem Description:
A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store 
and retrieve keys in a dataset of strings. There are various applications of this data structure, 
such as autocomplete and spellchecker.

Implement the Trie class:
- `Trie()` Initializes the trie object.
- `void insert(String word)` Inserts string `word` into the trie.
- `boolean search(String word)` Returns `true` if string `word` is in trie, and `false` otherwise.
- `boolean startsWith(String prefix)` Returns `true` if there is a previously inserted string `word` 
  that has the prefix `prefix`, and `false` otherwise.
"""

from typing import Dict

class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Returns True if the word is in the trie.
        """
        curr = self.root
        for char in word:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return curr.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Returns True if there is any word in the trie that starts with prefix.
        """
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return True

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Trie...")
    
    trie = Trie()
    trie.insert("apple")
    
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.starts_with("app") is True
    
    trie.insert("app")
    assert trie.search("app") is True
    
    print("All tests passed successfully!")
