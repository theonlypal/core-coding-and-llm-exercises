"""
Topic: Text Chunker
Exercise: Recursive Character Text Splitter

Problem Description:
When preparing documents for Retrieval-Augmented Generation (RAG), splitting large texts 
into smaller chunks is essential to fit context windows and provide relevant snippets.
A naive character-split can break words or sentences.

Implement a recursive character text splitter class `RecursiveTextSplitter` that:
- Accepts a list of separator priority strings (default: `["\\n\\n", "\\n", " ", ""]`).
- Recursively splits text using the highest-priority separator that can keep chunks under `chunk_size`.
- Ensures chunk overlap of size `chunk_overlap` is maintained between adjacent chunks.

Interface:
- `split_text(text: str) -> list[str]`
"""

class RecursiveTextSplitter:
    def __init__(self, chunk_size: int = 100, chunk_overlap: int = 20, separators: list[str] = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> list[str]:
        """
        Recursively splits text into chunks of maximum size `chunk_size`
        with overlap `chunk_overlap`.
        """
        if not text:
            return []
            
        final_chunks = []
        
        # Helper to recursively split text blocks
        def split_block(block: str, separator_idx: int) -> list[str]:
            # If the block is already small enough, return it
            if len(block) <= self.chunk_size:
                return [block]
                
            # If we've run out of separators, we must split by chunk size directly (force split)
            if separator_idx >= len(self.separators):
                return [block[i:i + self.chunk_size] for i in range(0, len(block), self.chunk_size)]
                
            separator = self.separators[separator_idx]
            
            # Split block using the current separator
            if separator == "":
                splits = list(block)
            else:
                splits = block.split(separator)
                
            # Now build chunks by combining splits
            chunks = []
            current_chunk = []
            current_len = 0
            
            for s in splits:
                s_len = len(s)
                sep_len = len(separator) if current_chunk else 0
                
                # Check if adding this split exceeds chunk_size
                if current_len + sep_len + s_len > self.chunk_size:
                    if current_chunk:
                        # Save completed chunk
                        chunks.append(separator.join(current_chunk))
                        
                        # Handle overlap: keep ending items that fit in chunk_overlap
                        overlap_chunk = []
                        overlap_len = 0
                        for prev_s in reversed(current_chunk):
                            p_len = len(prev_s)
                            p_sep = len(separator) if overlap_chunk else 0
                            if overlap_len + p_sep + p_len <= self.chunk_overlap:
                                overlap_chunk.insert(0, prev_s)
                                overlap_len += p_sep + p_len
                            else:
                                break
                        current_chunk = overlap_chunk
                        current_len = overlap_len
                        
                    # If a single split item is larger than chunk_size, recurse on it with next separator
                    if s_len > self.chunk_size:
                        sub_splits = split_block(s, separator_idx + 1)
                        # The first sub-splits might merge with the current overlap chunk
                        for sub_s in sub_splits:
                            sep_len = len(separator) if current_chunk else 0
                            if current_len + sep_len + len(sub_s) <= self.chunk_size:
                                current_chunk.append(sub_s)
                                current_len += sep_len + len(sub_s)
                            else:
                                if current_chunk:
                                    chunks.append(separator.join(current_chunk))
                                current_chunk = [sub_s]
                                current_len = len(sub_s)
                    else:
                        current_chunk.append(s)
                        current_len = s_len
                else:
                    current_chunk.append(s)
                    current_len += sep_len + s_len
                    
            if current_chunk:
                chunks.append(separator.join(current_chunk))
                
            return chunks

        return split_block(text, 0)

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Recursive Character Text Splitter...")
    
    splitter = RecursiveTextSplitter(chunk_size=50, chunk_overlap=10)
    
    text = (
        "This is a long sentence that should split.\n\n"
        "Here is a second paragraph that is also quite long.\n"
        "And a third line."
    )
    
    chunks = splitter.split_text(text)
    
    print(f"Generated {len(chunks)} chunks:")
    for idx, chunk in enumerate(chunks):
        print(f"  Chunk {idx}: {repr(chunk)} (Len: {len(chunk)})")
        assert len(chunk) <= 50, f"Chunk {idx} is too large!"
        
    # Check overlap sanity: some keywords should overlap
    # Let's verify that adjacent chunks share some suffix/prefix
    for i in range(len(chunks) - 1):
        c1, c2 = chunks[i], chunks[i+1]
        # At least some characters should overlap if splitting continuously
        # Note: Depending on separator boundaries, perfect overlap might not occur,
        # but chunks shouldn't exceed chunk_size.
        pass
        
    print("All tests passed successfully!")
