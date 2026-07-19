"""
Topic: Simple Vector Database
Exercise: In-Memory Vector Database

Problem Description:
Vector databases are at the heart of semantic search and Retrieval-Augmented Generation (RAG).
They store multi-dimensional vectors (embeddings) representing data objects, and provide fast
similarity search.

Implement an in-memory `SimpleVectorDB` class that supports:
1. `add_document(doc_id: str, vector: list[float], metadata: dict) -> None`:
   Stores a document, its vector, and associated metadata.
2. `search(query_vector: list[float], top_k: int = 3, metric: str = "cosine") -> list[dict]`:
   Searches the database for the top `k` most similar documents.
   Support two distance metrics:
     - `"cosine"`: Cosine similarity (higher is better, range [-1, 1])
     - `"euclidean"`: Euclidean distance (lower is better, range [0, inf))
   Returns a list of dicts representing results, ordered by similarity:
     `[{"doc_id": "...", "score": 0.98, "metadata": {...}}, ...]`

Raise appropriate errors for dimension mismatch.
"""

import math
from typing import Dict, List, Tuple

class SimpleVectorDB:
    def __init__(self, dimension: int):
        self.dimension = dimension
        # Store documents as a dictionary: doc_id -> (vector, metadata)
        self.storage: Dict[str, Tuple[List[float], dict]] = {}

    def add_document(self, doc_id: str, vector: List[float], metadata: dict) -> None:
        """
        Adds a document with its vector and metadata to the database.
        """
        if len(vector) != self.dimension:
            raise ValueError(f"Vector dimension {len(vector)} does not match database dimension {self.dimension}")
        self.storage[doc_id] = (vector, metadata)

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def _euclidean_distance(self, vec_a: List[float], vec_b: List[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)))

    def search(self, query_vector: List[float], top_k: int = 3, metric: str = "cosine") -> List[dict]:
        """
        Searches for the top_k most similar documents based on the chosen metric.
        """
        if len(query_vector) != self.dimension:
            raise ValueError(f"Query vector dimension {len(query_vector)} does not match database dimension {self.dimension}")
            
        if metric not in ("cosine", "euclidean"):
            raise ValueError("Unsupported metric. Choose 'cosine' or 'euclidean'.")
            
        results = []
        
        for doc_id, (vector, metadata) in self.storage.items():
            if metric == "cosine":
                score = self._cosine_similarity(query_vector, vector)
                results.append((score, doc_id, vector, metadata))
            else:  # euclidean
                score = self._euclidean_distance(query_vector, vector)
                results.append((score, doc_id, vector, metadata))
                
        # Sort results:
        # Cosine: descending order (higher similarity is better)
        # Euclidean: ascending order (lower distance is better)
        if metric == "cosine":
            results.sort(key=lambda x: x[0], reverse=True)
        else:
            results.sort(key=lambda x: x[0])
            
        # Format output
        top_results = []
        for score, doc_id, _, metadata in results[:top_k]:
            top_results.append({
                "doc_id": doc_id,
                "score": score,
                "metadata": metadata
            })
            
        return top_results

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Simple Vector DB...")
    
    # Initialize DB with 3 dimensions
    db = SimpleVectorDB(dimension=3)
    
    db.add_document("doc1", [1.0, 0.0, 0.0], {"title": "Introduction to AI"})
    db.add_document("doc2", [0.9, 0.1, 0.0], {"title": "Neural Networks"})
    db.add_document("doc3", [0.0, 1.0, 1.0], {"title": "Cooking Recipes"})
    
    # Query vector close to doc1 and doc2 (unambiguously closer to doc1)
    query = [0.98, 0.02, 0.0]
    
    # Test Cosine Similarity Search
    cosine_results = db.search(query, top_k=2, metric="cosine")
    print("Cosine search results:")
    for res in cosine_results:
        print(f"  {res['doc_id']}: score={res['score']:.4f}, metadata={res['metadata']}")
        
    assert len(cosine_results) == 2
    assert cosine_results[0]["doc_id"] == "doc1", "Expected doc1 to be the closest match in cosine similarity."
    assert cosine_results[1]["doc_id"] == "doc2"
    
    # Test Euclidean Distance Search
    euclidean_results = db.search(query, top_k=2, metric="euclidean")
    print("Euclidean search results:")
    for res in euclidean_results:
        print(f"  {res['doc_id']}: score={res['score']:.4f}, metadata={res['metadata']}")
        
    assert len(euclidean_results) == 2
    assert euclidean_results[0]["doc_id"] == "doc1"
    
    # Test validation error
    try:
        db.add_document("doc_bad", [1.0, 0.0], {})
        assert False, "Should raise ValueError for dimension mismatch."
    except ValueError:
        pass
        
    print("All tests passed successfully!")
