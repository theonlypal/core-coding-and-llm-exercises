"""
Topic: Long-Context Summarization
Exercise: Map-Reduce and Refine Summarization Pipelines

Problem Description:
Summarizing documents larger than an LLM's context window requires structured strategies:
1. **Map-Reduce**: Split text into chunks, summarize each chunk independently (Map), 
   then merge all chunk summaries into a final overview (Reduce).
2. **Refine**: Summarize chunk 1, then pass chunk 2 + summary 1 to update/refine summary 2, 
   iteratively updating the summary as new chunks are ingested.

Implement a `LongContextSummarizer` class containing:
1. `map_reduce_summarize(chunks: list[str], mock_llm_fn: Callable[[str], str]) -> str`:
   Executes Map-Reduce summarization.
2. `refine_summarize(chunks: list[str], mock_llm_fn: Callable[[str], str]) -> str`:
   Executes sequential Refine summarization.
"""

from typing import List, Callable

class LongContextSummarizer:
    def __init__(self):
        pass

    def map_reduce_summarize(self, chunks: List[str], mock_llm_fn: Callable[[str], str]) -> str:
        """
        Map-Reduce: Summarize each chunk independently, then combine.
        """
        if not chunks:
            return ""

        # Map Phase: Summarize each chunk
        chunk_summaries = []
        for idx, chunk in enumerate(chunks):
            prompt = f"Summarize chunk {idx + 1}: {chunk}"
            summary = mock_llm_fn(prompt)
            chunk_summaries.append(summary)

        # Reduce Phase: Combine summaries
        combined_summaries = "\n".join(chunk_summaries)
        reduce_prompt = f"Create a master summary from these sub-summaries:\n{combined_summaries}"
        final_summary = mock_llm_fn(reduce_prompt)

        return final_summary

    def refine_summarize(self, chunks: List[str], mock_llm_fn: Callable[[str], str]) -> str:
        """
        Refine: Sequentially refine summary as each new chunk is ingested.
        """
        if not chunks:
            return ""

        # Step 1: Initial summary for chunk 0
        current_summary = mock_llm_fn(f"Summarize initial chunk: {chunks[0]}")

        # Step 2: Iteratively refine with remaining chunks
        for idx in range(1, len(chunks)):
            refine_prompt = (
                f"Existing Summary:\n{current_summary}\n\n"
                f"New Context (Chunk {idx + 1}):\n{chunks[idx]}\n\n"
                "Refine the existing summary incorporating the new context:"
            )
            current_summary = mock_llm_fn(refine_prompt)

        return current_summary

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Long-Context Summarizer...")

    summarizer = LongContextSummarizer()

    chunks = [
        "Chapter 1: Alice enters the mysterious forest and meets a talking cat.",
        "Chapter 2: The cat guides Alice to a hidden castle full of riddles.",
        "Chapter 3: Alice solves the castle riddles and discovers a magic key."
    ]

    # Simple mock LLM summary function
    def mock_llm(prompt: str) -> str:
        if "reduce" in prompt.lower() or "master summary" in prompt.lower():
            return "Master Summary: Alice meets a cat in the forest, explores a castle, and finds a magic key."
        elif "refine" in prompt.lower():
            return "Refined Summary: Alice explores forest and castle with a cat, unlocking a magic key."
        elif "chunk 1" in prompt.lower() or "initial chunk" in prompt.lower():
            return "Alice enters forest, meets cat."
        elif "chunk 2" in prompt.lower():
            return "Cat leads Alice to riddle castle."
        elif "chunk 3" in prompt.lower():
            return "Alice solves riddles, gets magic key."
        return "Summary of text."

    # Test Map-Reduce Strategy
    mr_result = summarizer.map_reduce_summarize(chunks, mock_llm)
    print(f"Map-Reduce Summary: '{mr_result}'")
    assert "Master Summary" in mr_result

    # Test Refine Strategy
    refine_result = summarizer.refine_summarize(chunks, mock_llm)
    print(f"Refine Summary: '{refine_result}'")
    assert "Refined Summary" in refine_result

    print("All tests passed successfully!")
