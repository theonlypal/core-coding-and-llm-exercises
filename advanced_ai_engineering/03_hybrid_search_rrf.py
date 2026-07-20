"""
Topic: Hybrid Search Engine with Reciprocal Rank Fusion (RRF)
Exercise: Keyword + Vector Search Fusion

Problem Description:
Pure vector search can miss exact keyword matches (like part numbers or names), while pure 
keyword search (BM25) misses semantic intent. Hybrid Search runs both search strategies and 
fuses their ranked result lists using Reciprocal Rank Fusion (RRF).

RRF Formula:
Score(doc) = sum( 1 / (k + rank_in_system_i) ) for each search system i.
Standard constant k is typically 60.

Implement a `HybridSearchEngine` class containing:
1. `bm25_search(query: str, top_n: int) -> list[tuple[str, float]]`:
   Calculates term frequency-based keyword match ranks for documents.
2. `vector_search(query_vec: list[float], top_n: int) -> list[tuple[str, float]]`:
   Calculates cosine similarity vector search ranks for documents.
3. `reciprocal_rank_fusion(rankings: list[list[tuple[str, float]]], k: int = 60) -> list[tuple[str, float]]`:
   Combines multiple ranked lists into a single fused score list sorted descending.
"""

import math
import re
from typing import Dict, List, Tuple

class HybridSearchEngine:
    def __init__(self, k_rrf: int = 60):
        self.k_rrf = k_rrf
        # doc_id -> text
        self.documents: Dict[str, str] = {}
        # doc_id -> embedding vector
        self.doc_vectors: Dict[str, List[float]] = {}

    def add_document(self, doc_id: str, text: str, vector: List[float]) -> None:
        self.documents[doc_id] = text
        self.doc_vectors[doc_id] = vector

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def bm25_search(self, query: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Calculates keyword match scores based on term frequency overlap.
        """
        q_tokens = set(self._tokenize(query))
        scores = []
        
        for doc_id, text in self.documents.items():
            doc_tokens = self._tokenize(text)
            if not doc_tokens:
                continue
            # Term Frequency score
            tf_score = sum(doc_tokens.count(tok) for tok in q_tokens)
            scores.append((doc_id, float(tf_score)))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]

    def vector_search(self, query_vec: List[float], top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Calculates Cosine Similarity vector search scores.
        """
        scores = []
        q_norm = math.sqrt(sum(x * x for x in query_vec))
        
        for doc_id, vec in self.doc_vectors.items():
            dot = sum(a * b for a, b in zip(query_vec, vec))
            v_norm = math.sqrt(sum(y * y for y in vec))
            sim = dot / (q_norm * v_norm) if q_norm and v_norm else 0.0
            scores.append((doc_id, sim))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]

    def reciprocal_rank_fusion(
        self, 
        ranked_lists: List[List[Tuple[str, float]]]
    ) -> List[Tuple[str, float]]:
        """
        Combines multiple ranked lists using RRF score formula: sum( 1 / (k + rank) ).
        Ranks are 1-indexed.
        """
        rrf_scores: Dict[str, float] = {}
        
        for ranked_list in ranked_lists:
            for rank_0, (doc_id, _) in enumerate(ranked_list):
                rank = rank_0 + 1  # 1-indexed rank
                rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.k_rrf + rank))
                
        fused_results = [(doc_id, score) for doc_id, score in rrf_scores.items()]
        fused_results.sort(key=lambda x: x[1], reverse=True)
        return fused_results

    def hybrid_search(self, query: str, query_vec: List[float], top_n: int = 3) -> List[Tuple[str, float]]:
        bm25_ranks = self.bm25_search(query, top_n=top_n * 2)
        vec_ranks = self.vector_search(query_vec, top_n=top_n * 2)
        return self.reciprocal_rank_fusion([bm25_ranks, vec_ranks])[:top_n]

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Hybrid Search RRF...")
    
    engine = HybridSearchEngine(k_rrf=60)
    
    # Doc 1: Has exact keyword "ERR-404"
    engine.add_document("doc1", "System error code ERR-404 in server logs.", [0.1, 0.9, 0.0])
    # Doc 2: Has high semantic similarity to "connection issues" but missing exact code
    engine.add_document("doc2", "Network connectivity timeout on remote host database.", [0.95, 0.05, 0.0])
    # Doc 3: Unrelated
    engine.add_document("doc3", "Recipe for chocolate chip cookies.", [0.0, 0.0, 1.0])
    
    query_str = "ERR-404 connectivity timeout"
    query_vector = [0.9, 0.1, 0.0]
    
    bm25_res = engine.bm25_search(query_str)
    vec_res = engine.vector_search(query_vector)
    hybrid_res = engine.hybrid_search(query_str, query_vector, top_n=2)
    
    print(f"BM25 Ranks: {bm25_res}")
    print(f"Vector Ranks: {vec_res}")
    print(f"Hybrid RRF Ranks: {hybrid_res}")
    
    assert len(hybrid_res) == 2
    # Both doc1 and doc2 should feature in top hybrid search results
    doc_ids = [r[0] for r in hybrid_res]
    assert "doc1" in doc_ids and "doc2" in doc_ids
    
    print("All tests passed successfully!")
