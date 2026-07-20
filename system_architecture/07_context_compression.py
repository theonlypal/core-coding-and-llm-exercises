"""
Topic: Context Compression
Exercise: Prompt Token Compaction and Information Density Optimization

Problem Description:
Long prompts increase LLM costs and latency. Context compression techniques remove filler words, 
stop words, and low-relevance sentences while preserving critical core facts.

Implement a `ContextCompressor` class containing:
1. `remove_stop_words(text: str) -> str`:
   Removes common stop words ("a", "an", "the", "is", "in", "at", "of", "and").
2. `compress_by_relevance(text: str, query: str, max_chars: int) -> str`:
   Ranks sentences by term-overlap relevance to query, selecting top sentences fitting within `max_chars`.
"""

import re
from typing import List, Set

class ContextCompressor:
    def __init__(self):
        self.stop_words: Set[str] = {
            "a", "an", "the", "is", "are", "was", "were", "in", "on", 
            "at", "of", "for", "to", "with", "and", "or", "it", "this", "that"
        }

    def remove_stop_words(self, text: str) -> str:
        words = text.split()
        filtered = [w for w in words if w.lower().strip(",.!?") not in self.stop_words]
        return " ".join(filtered)

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def compress_by_relevance(self, text: str, query: str, max_chars: int) -> str:
        """
        Extracts top sentences relevant to query that fit inside max_chars limit.
        """
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        q_tokens = set(self._tokenize(query))

        scored_sentences = []
        for idx, sent in enumerate(sentences):
            s_tokens = self._tokenize(sent)
            score = sum(s_tokens.count(t) for t in q_tokens)
            # Preserves original order (idx) on equal score
            scored_sentences.append((score, idx, sent))

        # Sort by relevance score descending
        scored_sentences.sort(key=lambda x: (x[0], -x[1]), reverse=True)

        selected_sentences = []
        current_len = 0

        for score, idx, sent in scored_sentences:
            if current_len + len(sent) + 1 <= max_chars:
                selected_sentences.append((idx, sent))
                current_len += len(sent) + 1

        # Re-sort selected sentences by original document index
        selected_sentences.sort(key=lambda x: x[0])
        return " ".join(sent for _, sent in selected_sentences)

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Context Compression...")

    compressor = ContextCompressor()

    # 1. Stop Words Removal Test
    raw_text = "The quick brown fox is jumping over an extremely lazy dog."
    cleaned = compressor.remove_stop_words(raw_text)
    print(f"Original ({len(raw_text)} chars): '{raw_text}'")
    print(f"Cleaned ({len(cleaned)} chars): '{cleaned}'")

    assert "the" not in cleaned.lower().split()
    assert "is" not in cleaned.lower().split()
    assert "quick" in cleaned

    # 2. Relevance Compression Test
    long_document = (
        "We discuss revenue figures in section 1. "
        "The server deployment encountered a network timeout error on port 8080. "
        "Employee benefits include health insurance and paid leave. "
        "The server network logs indicate high packet loss."
    )
    query = "server network error timeout"

    # Restrict output to 120 chars max
    compressed = compressor.compress_by_relevance(long_document, query, max_chars=140)
    print(f"Compressed Output:\n'{compressed}' (Len: {len(compressed)})")

    assert len(compressed) <= 140
    assert "server deployment encountered" in compressed
    assert "Employee benefits" not in compressed

    print("All tests passed successfully!")
