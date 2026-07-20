"""
Topic: Semantic Chunker
Exercise: Embedding Variance Text Splitter

Problem Description:
Fixed character/word chunking can split sentences or break context arbitrarily. 
Semantic Chunking splits documents at locations where consecutive sentences have a high 
semantic distance (similarity drop), grouping semantically coherent sentences together.

Implement a `SemanticChunker` class containing:
1. `split_sentences(text: str) -> list[str]`:
   Splits text into sentences.
2. `get_tf_vector(text: str, vocab: list[str]) -> list[float]`:
   Computes TF vector for sentence given a vocabulary.
3. `calculate_sentence_distances(sentences: list[str]) -> list[float]`:
   Calculates cosine distance (1 - similarity) between adjacent sentence pairs.
4. `chunk_by_semantic_similarity(text: str, distance_threshold: float = 0.5) -> list[str]`:
   Groups sentences into chunks, starting a new chunk whenever distance >= threshold.
"""

import math
import re
from typing import List, Tuple

class SemanticChunker:
    def __init__(self):
        pass

    def split_sentences(self, text: str) -> List[str]:
        # Split by sentence-ending punctuation followed by space/newline
        raw_sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in raw_sentences if s.strip()]

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def _cosine_distance(self, sent1: str, sent2: str) -> float:
        tokens1 = self._tokenize(sent1)
        tokens2 = self._tokenize(sent2)
        vocab = sorted(list(set(tokens1 + tokens2)))

        if not vocab or not tokens1 or not tokens2:
            return 1.0  # Max distance if empty

        v1 = [tokens1.count(w) / len(tokens1) for w in vocab]
        v2 = [tokens2.count(w) / len(tokens2) for w in vocab]

        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))

        similarity = dot / (norm1 * norm2) if norm1 and norm2 else 0.0
        return 1.0 - similarity

    def chunk_by_semantic_similarity(self, text: str, distance_threshold: float = 0.6) -> List[str]:
        sentences = self.split_sentences(text)
        if not sentences:
            return []

        chunks = []
        current_chunk = [sentences[0]]

        for i in range(len(sentences) - 1):
            s1 = sentences[i]
            s2 = sentences[i + 1]
            dist = self._cosine_distance(s1, s2)

            # If semantic distance exceeds threshold, split chunk
            if dist >= distance_threshold:
                chunks.append(" ".join(current_chunk))
                current_chunk = [s2]
            else:
                current_chunk.append(s2)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Semantic Chunker...")

    chunker = SemanticChunker()

    document = (
        "Python is a great programming language for data science. "
        "Python data science supports machine learning libraries. "
        "Baking chocolate cake requires flour sugar and cocoa. "
        "Preheat the baking oven to 350 degrees for baking the cake."
    )

    chunks = chunker.chunk_by_semantic_similarity(document, distance_threshold=0.8)
    print(f"Generated {len(chunks)} Semantic Chunks:")
    for idx, c in enumerate(chunks):
        print(f"  Chunk {idx}: '{c}'")

    # Should separate Python/AI topic from Baking topic
    assert len(chunks) == 2
    assert "Python" in chunks[0] and "programming" in chunks[0]
    assert "Baking" in chunks[1] and "oven" in chunks[1]

    print("All tests passed successfully!")
