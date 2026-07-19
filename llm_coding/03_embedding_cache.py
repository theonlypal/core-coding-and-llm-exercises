"""
Topic: Embedding Cache
Exercise: Thread-Safe Semantic Cache

Problem Description:
LLM API calls are expensive and slow. A Semantic Cache stores previous LLM prompts and their
responses. If a new prompt is semantically similar to a cached prompt (determined by computing
cosine similarity on their embeddings and checking against a threshold), the cached response
is returned immediately.

Implement a thread-safe `SemanticCache` class that supporting:
1. `lookup(query_embedding: list[float]) -> tuple[str, float] | None`:
   Given a query embedding, search cached items. Return a tuple of `(response, similarity)`
   for the most similar prompt if its cosine similarity is >= `threshold`. Otherwise, return `None`.
2. `insert(prompt: str, embedding: list[float], response: str) -> None`:
   Thread-safely insert a new prompt, its embedding, and the LLM response into the cache.

Cosine Similarity formula:
similarity = dot_product(A, B) / (norm(A) * norm(B))
"""

import math
import threading
from typing import List, Optional, Tuple

class SemanticCache:
    def __init__(self, threshold: float = 0.90):
        self.threshold = threshold
        self.lock = threading.Lock()
        # Storage format: list of dicts/tuples: (prompt, embedding, response)
        self.cache: List[Tuple[str, List[float], str]] = []

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Computes cosine similarity between two vectors.
        """
        if len(vec_a) != len(vec_b):
            raise ValueError("Vectors must be of the same dimension.")
            
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
            
        return dot_product / (norm_a * norm_b)

    def lookup(self, query_embedding: List[float]) -> Optional[Tuple[str, float]]:
        """
        Looks up a semantically similar response in the cache.
        Thread-safe read operation.
        """
        with self.lock:
            best_match = None
            best_similarity = -1.0
            
            for prompt, cached_emb, response in self.cache:
                similarity = self._cosine_similarity(query_embedding, cached_emb)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = response
                    
            if best_similarity >= self.threshold:
                return best_match, best_similarity
                
            return None

    def insert(self, prompt: str, embedding: List[float], response: str) -> None:
        """
        Inserts a prompt, its embedding, and the response into the cache.
        Thread-safe write operation.
        """
        with self.lock:
            self.cache.append((prompt, embedding, response))

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Semantic Cache...")
    
    # Simple 3-dimensional mock embeddings
    # E.g., representations of "fruits"
    apple_emb = [1.0, 0.1, 0.0]
    orange_emb = [0.95, 0.15, 0.0]  # Very similar to apple
    dog_emb = [0.0, 0.1, 1.0]       # Very different from apple
    
    cache = SemanticCache(threshold=0.92)
    
    # 1. Insert "What is an apple?" response
    cache.insert(
        prompt="What is an apple?",
        embedding=apple_emb,
        response="An apple is a sweet, edible fruit produced by an apple tree."
    )
    
    # 2. Look up similar prompt: "Tell me about apples (orange-like embedding)"
    match = cache.lookup(orange_emb)
    assert match is not None, "Expected semantic cache hit!"
    response, similarity = match
    print(f"Cache Hit! Similarity: {similarity:.4f}")
    print(f"Response: {response}")
    assert "sweet, edible fruit" in response
    
    # 3. Look up dissimilar prompt: "What is a dog?"
    miss = cache.lookup(dog_emb)
    assert miss is None, "Expected semantic cache miss for unrelated query."
    
    # 4. Verify thread safety
    def worker(cache_obj: SemanticCache, val: int):
        cache_obj.insert(f"prompt {val}", [float(val), 1.0], f"response {val}")
        
    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(cache, i))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    assert len(cache.cache) == 11, f"Expected 11 cached entries, got {len(cache.cache)}"
    
    print("All tests passed successfully!")
