"""
Topic: RAG Pipeline
Exercise: Mini RAG Pipeline from Scratch

Problem Description:
Retrieval-Augmented Generation (RAG) improves LLM responses by fetching relevant context
from a local document store.

Implement an end-to-end mini RAG pipeline containing:
1. `chunk_text(text: str, max_words: int = 15) -> list[str]`:
   Splits text into chunks of maximum `max_words` words.
2. `get_tfidf_embedding(text: str, vocabulary: list[str]) -> list[float]`:
   Computes a basic TF (Term Frequency) vector based on a vocabulary list.
   (Term Frequency = count of word / total words in text).
3. `cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float`:
   Calculates cosine similarity between two vectors.
4. `retrieve_context(query: str, chunks: list[str], vocab: list[str], top_k: int = 2) -> list[str]`:
   Embeds query and chunks, computes similarities, and returns the top_k matching chunks.
5. `assemble_prompt(query: str, contexts: list[str]) -> str`:
   Formats a final prompt containing the retrieved context and user query.
"""

import math
import re
from typing import List

def chunk_text(text: str, max_words: int = 15) -> List[str]:
    """
    Splits text into chunks of at most max_words, keeping words intact.
    """
    words = re.findall(r"\b\w+\b", text.lower())
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))
    return chunks

def build_vocabulary(chunks: List[str]) -> List[str]:
    """
    Helper to extract all unique words across all chunks.
    """
    vocab = set()
    for chunk in chunks:
        words = re.findall(r"\b\w+\b", chunk.lower())
        vocab.update(words)
    return sorted(list(vocab))

def get_tfidf_embedding(text: str, vocabulary: List[str]) -> List[float]:
    """
    Generates a Term Frequency (TF) vector for a text given a vocabulary.
    """
    words = re.findall(r"\b\w+\b", text.lower())
    if not words:
        return [0.0] * len(vocabulary)
        
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
        
    vector = []
    for term in vocabulary:
        vector.append(counts.get(term, 0) / len(words))
    return vector

def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Calculates the cosine similarity between two vectors.
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def retrieve_context(
    query: str, 
    chunks: List[str], 
    vocab: List[str], 
    top_k: int = 2
) -> List[str]:
    """
    Retrieves the top_k chunks most similar to the query.
    """
    q_vec = get_tfidf_embedding(query, vocab)
    scored_chunks = []
    
    for chunk in chunks:
        c_vec = get_tfidf_embedding(chunk, vocab)
        score = cosine_similarity(q_vec, c_vec)
        scored_chunks.append((score, chunk))
        
    # Sort by score descending
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in scored_chunks[:top_k]]

def assemble_prompt(query: str, contexts: List[str]) -> str:
    """
    Assembles a prompt using retrieved contexts.
    """
    context_str = "\n".join(f"- {c}" for c in contexts)
    return (
        "Answer the user query based ONLY on the following contexts:\n"
        f"{context_str}\n\n"
        f"Query: {query}\n"
        "Answer:"
    )

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for RAG Pipeline...")
    
    document = (
        "Python is a popular programming language. It is used for web development and data science. "
        "Dynamic programming is an optimization method. It solves complex problems by breaking them down. "
        "Vector databases store multi-dimensional embeddings for semantic search retrieval."
    )
    
    # 1. Chunking
    chunks = chunk_text(document, max_words=10)
    print(f"Chunks: {chunks}")
    assert len(chunks) > 2
    
    # 2. Vocabulary
    vocab = build_vocabulary(chunks)
    assert len(vocab) > 10
    
    # 3. Retrieval Test (should match third chunk about vector databases)
    query = "semantic search in vector databases"
    retrieved = retrieve_context(query, chunks, vocab, top_k=1)
    print(f"Query: '{query}' -> Retrieved: {retrieved}")
    assert "vector" in retrieved[0] or "databases" in retrieved[0]
    
    # 4. Prompt Assembly
    final_prompt = assemble_prompt(query, retrieved)
    print("Assembled Prompt:")
    print(final_prompt)
    assert "Answer the user query" in final_prompt
    assert query in final_prompt
    
    print("All tests passed successfully!")
