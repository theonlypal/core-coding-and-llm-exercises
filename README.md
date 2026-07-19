# Core Coding and LLM Engineering Exercises

שָׁרְט

A curated set of python coding challenges designed to prepare developers for AI-native Software Engineering and LLM Engineering roles.

This repository is split into two sections:
1. **Core Coding**: Classic data structure and algorithm (DSA) questions commonly tested in technical screens.
2. **LLM Coding**: Production-grade engineering challenges focused on working with large language models, streaming, tokenization, embeddings, vector databases, rate limits, concurrency, and validation.

---

## Directory Structure

### 1. Core Coding (`core_coding/`)
Each file includes the problem description, target complexity, templates, and self-verifying test cases:
*   [01_arrays_and_hashmaps.py](core_coding/01_arrays_and_hashmaps.py) — **Group Anagrams** (LeetCode 49)
*   [02_strings.py](core_coding/02_strings.py) — **Valid Palindrome** (LeetCode 125)
*   [03_trees.py](core_coding/03_trees.py) — **Binary Tree Traversal** (DFS: Max Depth, BFS: Level Order)
*   [04_graphs.py](core_coding/04_graphs.py) — **Number of Islands** (LeetCode 200)
*   [05_heaps.py](core_coding/05_heaps.py) — **Kth Largest Element in an Array** (LeetCode 215)
*   [06_binary_search.py](core_coding/06_binary_search.py) — **Search in Rotated Sorted Array** (LeetCode 33)
*   [07_sliding_window.py](core_coding/07_sliding_window.py) — **Longest Substring Without Repeating Characters** (LeetCode 3)
*   [08_dynamic_programming.py](core_coding/08_dynamic_programming.py) — **Coin Change** (LeetCode 322)
*   [09_backtracking.py](core_coding/09_backtracking.py) — **Generate Parentheses** (LeetCode 22)

### 2. LLM Coding (`llm_coding/`)
Practical, self-contained AI-native backend challenges implemented in pure Python:
*   [01_token_counting.py](llm_coding/01_token_counting.py) — **Byte-Pair Encoding (BPE) Tokenizer**: Merges frequencies and counts tokens.
*   [02_text_chunker.py](llm_coding/02_text_chunker.py) — **Recursive Character Text Splitter**: Chunks text with overlap boundaries.
*   [03_embedding_cache.py](llm_coding/03_embedding_cache.py) — **Thread-Safe Semantic Cache**: Bypasses LLM calls using cosine similarity.
*   [04_simple_vector_db.py](llm_coding/04_simple_vector_db.py) — **Simple In-Memory Vector DB**: Supports Cosine and Euclidean search.
*   [05_cosine_similarity.py](llm_coding/05_cosine_similarity.py) — **Cosine Similarity Engine**: Handles edge cases (zero vectors, dimensions).
*   [06_prompt_templates.py](llm_coding/06_prompt_templates.py) — **Prompt Template Engine**: Validates variables and formats chat structures.
*   [07_streaming_api.py](llm_coding/07_streaming_api.py) — **Mock LLM Streaming API**: Generator server and console stream consumer.
*   [08_rate_limiter.py](llm_coding/08_rate_limiter.py) — **Token Bucket Rate Limiter**: Thread-safe RPM/TPM control.
*   [09_exponential_backoff.py](llm_coding/09_exponential_backoff.py) — **Exponential Backoff Decorator**: Automatic retries with randomized jitter.
*   [10_parallel_llm_calls.py](llm_coding/10_parallel_llm_calls.py) — **Concurrent LLM Batch Processor**: Thread pool execution with safety limits.
*   [11_json_schema_validation.py](llm_coding/11_json_schema_validation.py) — **LLM JSON Schema Validator**: Validates structured output, auto-casts types.

---

## How to Use This Repository

Every file contains a completed, clean solution inside the main function, as well as a series of built-in tests at the bottom.

1. **Verify Solutions**: You can run any file directly using Python to see if the tests pass:
   ```bash
   python3 core_coding/01_arrays_and_hashmaps.py
   python3 llm_coding/01_token_counting.py
   ```
2. **Practice/Mock Interviews**: If you or a candidate wants to use these for practice, simply delete/comment out the bodies of the implementation functions (leaving the `pass` or `raise NotImplementedError`) and attempt to implement the solution such that all tests pass.

---

## Author & Contact
- **Name**: Rayan Pal
- **GitHub**: [theonlypal](https://github.com/theonlypal)
- **Email**: rpal@sandiego.edu
