"""
Topic: Tiered Agent Memory (MemGPT Architecture)
Exercise: 3-Tiered Memory Manager (Working, Episodic, and Archived)

Problem Description:
Agent context windows spill over if history isn't managed. MemGPT-style architectures split memory:
1. **Working Memory**: Fixed slots for core system context and persona/user variables (e.g. User Name).
2. **Episodic Memory**: Bounded queue of recent interaction events.
3. **Archived Memory**: Long-term vector-searchable store for past interactions pushed out of Episodic.

Implement a `TieredMemoryManager` class containing:
1. `update_working_memory(key: str, value: str) -> None`:
   Updates working memory key-value slots.
2. `add_event(role: str, content: str) -> None`:
   Adds event to Episodic queue. When size exceeds `max_episodic`, flushes oldest to Archived memory.
3. `search_archive(query: str, top_k: int = 1) -> list[str]`:
   Searches Archived Memory using TF vector similarity.
4. `compile_prompt_context(current_query: str) -> str`:
   Compiles Working Memory, Episodic Memory, and relevant Archived Memory into a prompt.
"""

import math
import re
from typing import Dict, List, Tuple

class TieredMemoryManager:
    def __init__(self, max_episodic: int = 3):
        self.max_episodic = max_episodic
        
        # 1. Working Memory: Key-Value dict (e.g., persona, core user traits)
        self.working_memory: Dict[str, str] = {}
        
        # 2. Episodic Memory: Recent event log queue
        self.episodic_memory: List[Dict[str, str]] = []
        
        # 3. Archived Memory: Archived events (stored as text strings for retrieval)
        self.archived_memory: List[str] = []

    def update_working_memory(self, key: str, value: str) -> None:
        self.working_memory[key] = value

    def _flush_oldest_episodic(self) -> None:
        oldest = self.episodic_memory.pop(0)
        archived_entry = f"[{oldest['role'].upper()}]: {oldest['content']}"
        self.archived_memory.append(archived_entry)

    def add_event(self, role: str, content: str) -> None:
        self.episodic_memory.append({"role": role, "content": content})
        if len(self.episodic_memory) > self.max_episodic:
            self._flush_oldest_episodic()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def search_archive(self, query: str, top_k: int = 1) -> List[str]:
        if not self.archived_memory:
            return []

        q_tokens = set(self._tokenize(query))
        scored = []

        for entry in self.archived_memory:
            entry_tokens = self._tokenize(entry)
            overlap = sum(entry_tokens.count(t) for t in q_tokens)
            scored.append((overlap, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry for score, entry in scored[:top_k] if score > 0]

    def compile_prompt_context(self, current_query: str) -> str:
        # 1. Format Working Memory
        wm_str = "\n".join(f"- {k}: {v}" for k, v in self.working_memory.items())
        
        # 2. Format Relevant Archived Memory
        relevant_archived = self.search_archive(current_query, top_k=2)
        arch_str = "\n".join(f"- {entry}" for entry in relevant_archived) if relevant_archived else "None"
        
        # 3. Format Episodic History
        ep_str = "\n".join(f"[{e['role']}]: {e['content']}" for e in self.episodic_memory)

        return (
            f"=== WORKING MEMORY ===\n{wm_str}\n\n"
            f"=== RELEVANT ARCHIVED MEMORY ===\n{arch_str}\n\n"
            f"=== EPISODIC CONVERSATION HISTORY ===\n{ep_str}\n\n"
            f"[user]: {current_query}\n"
            "[assistant]:"
        )

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Tiered Agent Memory...")

    mem = TieredMemoryManager(max_episodic=2)

    # Set Working Memory
    mem.update_working_memory("User Name", "Rayan")
    mem.update_working_memory("User Goal", "Build AI Systems")

    # Add Episodic Events (Max 2)
    mem.add_event("user", "My favorite programming language is Python.")
    mem.add_event("assistant", "Python is great for AI engineering!")
    mem.add_event("user", "I live in San Diego.")  # Flushes first event to Archive

    # Verify Flushing to Archive
    assert len(mem.episodic_memory) == 2
    assert len(mem.archived_memory) == 1
    assert "Python" in mem.archived_memory[0]

    # Search Archive
    arch_hits = mem.search_archive("programming language")
    assert len(arch_hits) == 1
    assert "Python" in arch_hits[0]

    # Compile Context
    compiled_prompt = mem.compile_prompt_context("What language do I like?")
    print("Compiled Context Prompt:")
    print(compiled_prompt)

    assert "Rayan" in compiled_prompt
    assert "Python" in compiled_prompt
    assert "San Diego" in compiled_prompt

    print("All tests passed successfully!")
