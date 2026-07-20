"""
Topic: KV Cache Simulator (Paged Attention)
Exercise: Block Memory Manager for Transformer KV Cache

Problem Description:
During LLM generation, Key-Value (KV) tensors for past tokens must be preserved to avoid 
re-computing self-attention. Naive contiguous memory pre-allocation causes severe memory fragmentation.
Paged Attention (used in vLLM) allocates physical memory blocks on-demand.

Implement a `PagedKVCacheManager` class containing:
1. `allocate_block() -> int`: Allocates a new block ID from a pool of free block IDs.
2. `append_token_kv(seq_id: str, key_vec: list[float], value_vec: list[float]) -> None`:
   Appends a token's KV tensors to a sequence's virtual block list, allocating new blocks when needed.
3. `get_sequence_kv(seq_id: str) -> tuple[list[list[float]], list[list[float]]]`:
   Retrieves all key and value vectors for a sequence across its allocated blocks in chronological order.
4. `calculate_memory_efficiency(seq_ids: list[str], max_seq_len: int) -> float`:
   Calculates the memory savings percentage of Paged Attention vs statically pre-allocating `max_seq_len` 
   memory blocks per sequence.
"""

from typing import Dict, List, Tuple, Optional

class PagedKVCacheManager:
    def __init__(self, block_size: int = 4, vector_dim: int = 128, total_blocks: int = 100):
        self.block_size = block_size
        self.vector_dim = vector_dim
        self.total_blocks = total_blocks
        
        # Free memory pool
        self.free_blocks: List[int] = list(range(total_blocks))
        
        # Physical memory storage: block_id -> list of (key_vec, val_vec) tuples
        self.physical_blocks: Dict[int, List[Tuple[List[float], List[float]]]] = {}
        
        # Mapping: seq_id -> list of physical block IDs allocated to sequence
        self.sequence_block_table: Dict[str, List[int]] = {}

    def allocate_block(self) -> int:
        if not self.free_blocks:
            raise MemoryError("Out of KV Cache physical memory blocks!")
        block_id = self.free_blocks.pop(0)
        self.physical_blocks[block_id] = []
        return block_id

    def append_token_kv(self, seq_id: str, key_vec: List[float], value_vec: List[float]) -> None:
        """
        Appends a token's KV vectors to sequence. Allocates a new block if current block is full.
        """
        if seq_id not in self.sequence_block_table:
            self.sequence_block_table[seq_id] = []
            
        block_list = self.sequence_block_table[seq_id]
        
        # If no blocks allocated or last block is full, allocate a new block
        if not block_list or len(self.physical_blocks[block_list[-1]]) >= self.block_size:
            new_block_id = self.allocate_block()
            block_list.append(new_block_id)
            
        current_block_id = block_list[-1]
        self.physical_blocks[current_block_id].append((key_vec, value_vec))

    def get_sequence_kv(self, seq_id: str) -> Tuple[List[List[float]], List[List[float]]]:
        """
        Retrieves all key and value vectors for a sequence in chronological order.
        """
        if seq_id not in self.sequence_block_table:
            return [], []
            
        keys, values = [], []
        for block_id in self.sequence_block_table[seq_id]:
            for k_vec, v_vec in self.physical_blocks[block_id]:
                keys.append(k_vec)
                values.append(v_vec)
                
        return keys, values

    def calculate_memory_efficiency(self, seq_ids: List[str], max_seq_len: int) -> float:
        """
        Returns memory waste reduction ratio (0.0 to 1.0) compared to naive max_seq_len pre-allocation.
        """
        # Static pre-allocation blocks needed
        # Naive approach allocates max_seq_len slots per sequence
        naive_slots = len(seq_ids) * max_seq_len
        
        # Actual slots allocated in Paged KV Cache
        actual_slots = sum(len(self.sequence_block_table[s]) * self.block_size for s in seq_ids)
        
        saved_slots = naive_slots - actual_slots
        return saved_slots / naive_slots if naive_slots > 0 else 0.0

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for KV Cache Simulator...")
    
    # Block size of 2 tokens per block, 128-dim vector
    cache_mgr = PagedKVCacheManager(block_size=2, vector_dim=128, total_blocks=50)
    
    # Sequence A: 3 tokens
    mock_k = [1.0] * 128
    mock_v = [2.0] * 128
    
    for _ in range(3):
        cache_mgr.append_token_kv("seq_A", mock_k, mock_v)
        
    # Sequence B: 1 token
    cache_mgr.append_token_kv("seq_B", mock_k, mock_v)
    
    # Verify allocation:
    # seq_A has 3 tokens -> block size 2 -> requires 2 blocks (4 slots allocated, 3 used)
    # seq_B has 1 token -> block size 2 -> requires 1 block (2 slots allocated, 1 used)
    assert len(cache_mgr.sequence_block_table["seq_A"]) == 2
    assert len(cache_mgr.sequence_block_table["seq_B"]) == 1
    
    keys_A, vals_A = cache_mgr.get_sequence_kv("seq_A")
    assert len(keys_A) == 3
    assert len(vals_A) == 3
    
    # Memory efficiency vs static max length of 16 tokens per sequence
    savings = cache_mgr.calculate_memory_efficiency(["seq_A", "seq_B"], max_seq_len=16)
    print(f"Memory savings over static pre-allocation: {savings * 100:.2f}%")
    # Naive: 2 * 16 = 32 slots. Actual: 3 blocks * 2 = 6 slots. Savings: 26/32 = 81.25%
    assert savings == 26 / 32
    
    print("All tests passed successfully!")
