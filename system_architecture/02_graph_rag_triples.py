"""
Topic: GraphRAG & Knowledge Graph Traversal
Exercise: Entity-Relation Triple Extraction & Multi-Hop Retrieval

Problem Description:
Standard RAG relies on semantic chunk similarity, failing on complex multi-hop queries. 
GraphRAG builds a Knowledge Graph of (Subject, Relation, Object) triples to allow multi-hop 
graph traversal alongside vector retrieval.

Implement a `GraphRAGStore` class containing:
1. `add_triple(subj: str, rel: str, obj: str, source_text: str) -> None`:
   Adds a directed edge between subject and object with a relation label.
2. `get_multihop_neighbors(start_node: str, max_depth: int = 2) -> set[str]`:
   Traverses the Knowledge Graph up to `max_depth` hops starting from `start_node`.
3. `retrieve_graph_context(entity: str, max_depth: int = 2) -> list[str]`:
   Returns all source text snippets connected to the entity within max_depth hops.
"""

from collections import deque, defaultdict
from typing import Dict, List, Set, Tuple

class GraphRAGStore:
    def __init__(self):
        # adj_list: node -> list of (neighbor_node, relation, source_text)
        self.adj_list: Dict[str, List[Tuple[str, str, str]]] = defaultdict(list)

    def add_triple(self, subj: str, rel: str, obj: str, source_text: str) -> None:
        subj_clean = subj.strip().lower()
        obj_clean = obj.strip().lower()
        rel_clean = rel.strip().lower()
        
        self.adj_list[subj_clean].append((obj_clean, rel_clean, source_text))
        # Add reverse edge for undirected exploration
        self.adj_list[obj_clean].append((subj_clean, f"rev_{rel_clean}", source_text))

    def get_multihop_neighbors(self, start_node: str, max_depth: int = 2) -> Set[str]:
        start = start_node.strip().lower()
        if start not in self.adj_list:
            return set()

        visited = {start}
        queue = deque([(start, 0)])

        while queue:
            node, depth = queue.popleft()
            if depth < max_depth:
                for neighbor, _, _ in self.adj_list[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, depth + 1))

        return visited

    def retrieve_graph_context(self, entity: str, max_depth: int = 2) -> List[str]:
        start = entity.strip().lower()
        neighbors = self.get_multihop_neighbors(start, max_depth)
        contexts = set()

        for node in neighbors:
            for neighbor, rel, src_text in self.adj_list[node]:
                if neighbor in neighbors:
                    contexts.add(src_text)

        return list(contexts)

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for GraphRAG Triples...")

    graph = GraphRAGStore()

    # Triple 1: Company X acquired Company Y
    graph.add_triple("Company X", "acquired", "Company Y", "In 2024, Company X acquired Company Y for $1B.")
    # Triple 2: Company Y manufactures Chip Z (Multi-hop link: Company X -> Company Y -> Chip Z)
    graph.add_triple("Company Y", "manufactures", "Chip Z", "Company Y manufactures high-performance Chip Z.")

    # 1. Test 1-hop neighbors of "Company X"
    one_hop = graph.get_multihop_neighbors("Company X", max_depth=1)
    assert "company y" in one_hop
    assert "chip z" not in one_hop

    # 2. Test 2-hop multi-hop neighbors of "Company X"
    two_hop = graph.get_multihop_neighbors("Company X", max_depth=2)
    assert "company y" in two_hop
    assert "chip z" in two_hop

    # 3. Retrieve multi-hop graph context
    contexts = graph.retrieve_graph_context("Company X", max_depth=2)
    print(f"Retrieved Graph Contexts ({len(contexts)}):")
    for c in contexts:
        print(f"  - {c}")

    assert len(contexts) == 2
    assert any("Chip Z" in c for c in contexts)

    print("All tests passed successfully!")
