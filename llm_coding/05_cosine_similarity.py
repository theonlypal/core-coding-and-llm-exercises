"""
Topic: Cosine Similarity Search
Exercise: Cosine Similarity Engine

Problem Description:
Cosine similarity measures the similarity between two non-zero vectors of an inner product space.
It measures the cosine of the angle between them, which determines whether they point in 
roughly the same direction. It is defined as:
    similarity = (A . B) / (||A|| * ||B||)

Implement a robust function `cosine_similarity_search` that:
1. Takes a `query_vector` (list of floats) and a dictionary of `documents` (dict mapping string ID -> list of floats).
2. Computes the cosine similarity of the query vector with every document vector.
3. Handles edge cases:
   - Zero vectors: if the query or any document vector has a magnitude of 0, its similarity should be defined as 0.0.
   - Dimension mismatch: raise a ValueError.
4. Returns the top `k` documents sorted by similarity score descending, including their scores.

Interface:
- `cosine_similarity_search(query_vector: list[float], documents: dict[str, list[float]], k: int = 3) -> list[tuple[str, float]]`
"""

import math
from typing import Dict, List, Tuple

def cosine_similarity_search(
    query_vector: List[float], 
    documents: Dict[str, List[float]], 
    k: int = 3
) -> List[Tuple[str, float]]:
    """
    Computes the cosine similarity between a query vector and a dict of document vectors,
    returning the top k matches sorted in descending order of similarity.
    """
    q_len = len(query_vector)
    
    # Calculate magnitude of query vector
    q_norm_sq = sum(x * x for x in query_vector)
    q_norm = math.sqrt(q_norm_sq)
    
    results = []
    
    for doc_id, doc_vector in documents.items():
        if len(doc_vector) != q_len:
            raise ValueError(f"Dimension mismatch for document '{doc_id}': expected {q_len}, got {len(doc_vector)}")
            
        # If query is zero vector, similarity is 0.0
        if q_norm == 0.0:
            results.append((doc_id, 0.0))
            continue
            
        # Calculate dot product and document magnitude
        dot_product = 0.0
        doc_norm_sq = 0.0
        for q_val, d_val in zip(query_vector, doc_vector):
            dot_product += q_val * d_val
            doc_norm_sq += d_val * d_val
            
        doc_norm = math.sqrt(doc_norm_sq)
        
        # If document is zero vector, similarity is 0.0
        if doc_norm == 0.0:
            similarity = 0.0
        else:
            similarity = dot_product / (q_norm * doc_norm)
            
        results.append((doc_id, similarity))
        
    # Sort by similarity score descending, and doc_id alphabetically on tie
    results.sort(key=lambda x: (x[1], x[0]), reverse=True)
    
    # Custom descending sort since we want reverse score but normal alphabetical order
    # To do that, we sort by (-score, doc_id) and don't reverse
    results.sort(key=lambda x: (-x[1], x[0]))
    
    return results[:k]

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Cosine Similarity Search...")
    
    documents = {
        "doc_a": [1.0, 1.0, 0.0],
        "doc_b": [1.0, 0.0, 1.0],
        "doc_c": [0.0, 0.0, 0.0],  # Zero vector
        "doc_d": [-1.0, -1.0, 0.0], # Opposite vector
    }
    
    # Query vector
    query = [1.0, 1.0, 0.0]
    
    # Top 3 matches
    results = cosine_similarity_search(query, documents, k=3)
    print("Results:")
    for doc_id, score in results:
        print(f"  {doc_id}: {score:.4f}")
        
    # Assertions
    assert results[0][0] == "doc_a"
    assert math.isclose(results[0][1], 1.0)
    
    # doc_b is [1, 0, 1], query is [1, 1, 0]. Similarity should be 1 / (sqrt(2) * sqrt(2)) = 0.5
    assert results[1][0] == "doc_b"
    assert math.isclose(results[1][1], 0.5)
    
    # doc_c is a zero vector, should have similarity 0.0
    assert results[2][0] == "doc_c"
    assert math.isclose(results[2][1], 0.0)
    
    # Query is zero vector test
    zero_query_results = cosine_similarity_search([0.0, 0.0, 0.0], documents, k=1)
    assert zero_query_results[0][1] == 0.0
    
    # Test dimension validation
    try:
        cosine_similarity_search([1.0, 0.0], documents)
        assert False, "Should raise ValueError for dimension mismatch."
    except ValueError:
        pass
        
    print("All tests passed successfully!")
