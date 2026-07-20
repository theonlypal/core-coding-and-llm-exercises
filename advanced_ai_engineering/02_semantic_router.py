"""
Topic: Semantic Router
Exercise: Intent Classification & Route Dispatcher

Problem Description:
Routing incoming user queries to specialized LLMs, prompts, or agents based on intent 
(e.g., math, code generation, greeting, general knowledge) reduces cost and latency.

Implement a `SemanticRouter` class containing:
1. `add_route(route_name: str, exemplars: list[str], handler: Callable[[str], str]) -> None`:
   Registers a route with example phrases and a callback handler.
2. `route_query(query: str, threshold: float = 0.5) -> str`:
   Calculates similarity between query and all route exemplars using term-frequency vectors.
   Executes the handler of the top-matching route if similarity >= threshold; otherwise uses default handler.
"""

import math
import re
from typing import Dict, List, Callable, Tuple, Optional

class SemanticRouter:
    def __init__(self, default_handler: Callable[[str], str]):
        self.default_handler = default_handler
        # route_name -> (exemplars, handler)
        self.routes: Dict[str, Tuple[List[str], Callable[[str], str]]] = {}
        self.vocabulary: List[str] = []

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def _update_vocab(self):
        vocab_set = set()
        for route_name, (exemplars, _) in self.routes.items():
            for ex in exemplars:
                vocab_set.update(self._tokenize(ex))
        self.vocabulary = sorted(list(vocab_set))

    def _get_tf_vector(self, text: str) -> List[float]:
        tokens = self._tokenize(text)
        if not tokens or not self.vocabulary:
            return [0.0] * len(self.vocabulary)
        counts = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        return [counts.get(word, 0) / len(tokens) for word in self.vocabulary]

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot / (norm_a * norm_b)

    def add_route(self, route_name: str, exemplars: List[str], handler: Callable[[str], str]) -> None:
        self.routes[route_name] = (exemplars, handler)
        self._update_vocab()

    def route_query(self, query: str, threshold: float = 0.3) -> str:
        """
        Routes the query to the best matching handler or default handler.
        """
        if not self.routes or not self.vocabulary:
            return self.default_handler(query)

        query_vec = self._get_tf_vector(query)
        best_score = -1.0
        best_handler = self.default_handler
        best_route = "default"

        for route_name, (exemplars, handler) in self.routes.items():
            for ex in exemplars:
                ex_vec = self._get_tf_vector(ex)
                score = self._cosine_similarity(query_vec, ex_vec)
                if score > best_score:
                    best_score = score
                    if score >= threshold:
                        best_handler = handler
                        best_route = route_name

        print(f"Query: '{query}' -> Best Route: '{best_route}' (Score: {best_score:.4f})")
        return best_handler(query)

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Semantic Router...")

    def default_bot(q: str) -> str:
        return "GENERAL: Processing general knowledge question."

    def math_bot(q: str) -> str:
        return "MATH: Solving mathematical equation."

    def code_bot(q: str) -> str:
        return "CODE: Executing code generator assistant."

    router = SemanticRouter(default_handler=default_bot)
    router.add_route("math", ["calculate sum plus minus divide multiply", "solve equation algebra math"], math_bot)
    router.add_route("code", ["write python function script class import def", "debug bug code syntax error"], code_bot)

    # 1. Test Math routing
    res_math = router.route_query("Please calculate the sum of 5 and 10", threshold=0.2)
    assert res_math.startswith("MATH:")

    # 2. Test Code routing
    res_code = router.route_query("Write a python function to sort a list", threshold=0.2)
    assert res_code.startswith("CODE:")

    # 3. Test Default routing
    res_default = router.route_query("What is the capital of France?", threshold=0.2)
    assert res_default.startswith("GENERAL:")

    print("All tests passed successfully!")
