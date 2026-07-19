"""
Topic: Token Counting
Exercise: Byte-Pair Encoding (BPE) Tokenizer

Problem Description:
Tokenization is the first step in processing text for LLMs. While libraries like tiktoken 
or HuggingFace's tokenizers are used in production, understanding the underlying algorithm 
(such as Byte-Pair Encoding) is crucial for AI engineers.

Implement a mini `SimpleBPETokenizer` class that can:
1. `train(text, vocab_size)`: Build a vocabulary of merges from a corpus.
2. `encode(text)`: Convert raw string into a list of token IDs.
3. `decode(ids)`: Reconstruct the raw string from token IDs.
4. `count_tokens(text)`: Returns the number of tokens for a given string.

Vocabulary Initialization:
Start with base characters as the initial vocabulary, and iteratively merge the most 
frequent adjacent pair of tokens until reaching `vocab_size` or no more pairs can be merged.
"""

import re
from typing import Dict, List, Tuple

class SimpleBPETokenizer:
    def __init__(self):
        # Maps token ID (int) -> byte representation (bytes)
        self.vocab: Dict[int, bytes] = {}
        # Maps byte/token pair (tuple of int) -> new token ID (int)
        self.merges: Dict[Tuple[int, int], int] = {}
        
    def train(self, text: str, vocab_size: int):
        """
        Trains BPE tokenizer on raw text.
        """
        # Convert text to bytes
        raw_bytes = text.encode("utf-8")
        # Initialize token IDs with individual byte values (0-255)
        ids = list(raw_bytes)
        
        # Base vocabulary is bytes 0 to 255
        self.vocab = {i: bytes([i]) for i in range(256)}
        
        # Determine number of merges to perform
        num_merges = vocab_size - 256
        new_token_id = 256
        
        for _ in range(num_merges):
            # 1. Count occurrences of adjacent pairs
            pair_counts = {}
            for i in range(len(ids) - 1):
                pair = (ids[i], ids[i+1])
                pair_counts[pair] = pair_counts.get(pair, 0) + 1
                
            if not pair_counts:
                break
                
            # Find the most frequent pair
            best_pair = max(pair_counts, key=pair_counts.get)
            
            # 2. Record the merge rule
            self.merges[best_pair] = new_token_id
            
            # Update vocabulary
            byte_val = self.vocab[best_pair[0]] + self.vocab[best_pair[1]]
            self.vocab[new_token_id] = byte_val
            
            # 3. Perform replacement of pair in ids list
            new_ids = []
            i = 0
            while i < len(ids):
                if i < len(ids) - 1 and (ids[i], ids[i+1]) == best_pair:
                    new_ids.append(new_token_id)
                    i += 2
                else:
                    new_ids.append(ids[i])
                    i += 1
            ids = new_ids
            new_token_id += 1

    def encode(self, text: str) -> List[int]:
        """
        Encodes a string into token IDs using learned merge rules.
        """
        ids = list(text.encode("utf-8"))
        
        # Repeatedly apply learned merges in the order they were learned
        # (simulating the greedy BPE encoding strategy)
        while len(ids) >= 2:
            # Find candidate pairs in current sequence
            pairs = [(ids[i], ids[i+1]) for i in range(len(ids) - 1)]
            
            # Find the pair with the lowest rank (earliest trained merge)
            # which matches our merges dictionary
            best_pair = None
            best_rank = float("inf")
            for pair in pairs:
                if pair in self.merges:
                    rank = self.merges[pair]
                    if rank < best_rank:
                        best_rank = rank
                        best_pair = pair
                        
            if best_pair is None:
                break  # No more mergeable pairs
                
            # Perform merge
            new_ids = []
            i = 0
            while i < len(ids):
                if i < len(ids) - 1 and (ids[i], ids[i+1]) == best_pair:
                    new_ids.append(self.merges[best_pair])
                    i += 2
                else:
                    new_ids.append(ids[i])
                    i += 1
            ids = new_ids
            
        return ids

    def decode(self, ids: List[int]) -> str:
        """
        Decodes a list of token IDs back to a string.
        """
        # Reconstruct byte sequence
        byte_chunks = []
        for token_id in ids:
            if token_id in self.vocab:
                byte_chunks.append(self.vocab[token_id])
            else:
                raise ValueError(f"Unknown token ID: {token_id}")
                
        # Decode as utf-8 (replace errors gracefully)
        return b"".join(byte_chunks).decode("utf-8", errors="replace")

    def count_tokens(self, text: str) -> int:
        """
        Counts the number of tokens in the given text.
        """
        return len(self.encode(text))

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for BPE Tokenizer...")
    
    tokenizer = SimpleBPETokenizer()
    training_corpus = "banana bandanna cabana standard tokenizer test banana bandanna"
    
    # Train vocabulary size up to 265 (9 merges)
    tokenizer.train(training_corpus, vocab_size=265)
    
    # Test encoding/decoding consistency
    test_str = "banana standard"
    encoded_ids = tokenizer.encode(test_str)
    decoded_str = tokenizer.decode(encoded_ids)
    
    print(f"Original: '{test_str}'")
    print(f"Encoded IDs: {encoded_ids}")
    print(f"Decoded: '{decoded_str}'")
    assert decoded_str == test_str, "Decoding did not match original text!"
    
    # Test count_tokens
    token_count = tokenizer.count_tokens("banana")
    # "banana" is frequent in the corpus so it should be heavily merged
    assert token_count < len("banana"), f"Expected compression, got {token_count} tokens."
    
    print("All tests passed successfully!")
