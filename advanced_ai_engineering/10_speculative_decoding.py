"""
Topic: Speculative Decoding Simulator
Exercise: Draft Model Inference Acceleration

Problem Description:
Large LLMs are memory-bandwidth bound during sequential token generation. 
Speculative decoding uses a fast, small **Draft Model** to generate $K$ speculative tokens, 
and a slow, large **Target Model** to verify all $K$ tokens in a single parallel forward pass.

Acceptance Rule:
Accept candidate token $i$ if $P_{target}(token_i) >= P_{draft}(token_i)$.
If rejected, stop generation at token $i$, replace it with a token sampled from Target Model, 
and discard remaining draft tokens.

Implement a `SpeculativeDecodingSimulator` class containing:
1. `verify_speculative_tokens(draft_tokens: list[str], draft_probs: list[float], target_probs: list[float]) -> tuple[list[str], int]`:
   Applies acceptance criteria to speculative draft tokens. Returns `(accepted_tokens, accepted_count)`.
2. `calculate_speedup_ratio(total_tokens_generated: int, total_target_passes: int) -> float`:
   Computes effective token generation speedup over standard serial target generation.
"""

from typing import List, Tuple

class SpeculativeDecodingSimulator:
    def __init__(self):
        pass

    def verify_speculative_tokens(
        self, 
        draft_tokens: List[str], 
        draft_probs: List[float], 
        target_probs: List[float]
    ) -> Tuple[List[str], int]:
        """
        Verifies draft tokens against target model probabilities.
        Stops at first rejected token.
        """
        if len(draft_tokens) != len(draft_probs) or len(draft_tokens) != len(target_probs):
            raise ValueError("Token lists and probability arrays must have equal length!")

        accepted_tokens = []
        
        for i in range(len(draft_tokens)):
            p_draft = draft_probs[i]
            p_target = target_probs[i]
            
            # Deterministic acceptance condition: p_target >= p_draft
            if p_target >= p_draft:
                accepted_tokens.append(draft_tokens[i])
            else:
                # Token rejected! Stop accepting further tokens
                print(f"Token {i} ('{draft_tokens[i]}') rejected: target prob {p_target:.2f} < draft prob {p_draft:.2f}")
                break
                
        return accepted_tokens, len(accepted_tokens)

    def calculate_speedup_ratio(self, total_tokens_generated: int, total_target_passes: int) -> float:
        """
        Calculates speedup ratio = total_tokens_generated / total_target_passes.
        (Standard generation yields 1 token per target pass = ratio 1.0).
        """
        if total_target_passes == 0:
            return 0.0
        return total_tokens_generated / total_target_passes

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Speculative Decoding Simulator...")

    simulator = SpeculativeDecodingSimulator()

    # Draft model generates 4 speculative tokens
    draft_tokens = ["The", "capital", "of", "France"]
    draft_probs = [0.80, 0.70, 0.90, 0.60]

    # Case 1: Target model agrees on first 3 tokens, but rejects 4th token ("France")
    target_probs_1 = [0.90, 0.85, 0.95, 0.40]

    accepted_1, count_1 = simulator.verify_speculative_tokens(draft_tokens, draft_probs, target_probs_1)
    print(f"Accepted Tokens Case 1: {accepted_1} (Count: {count_1})")

    assert count_1 == 3
    assert accepted_1 == ["The", "capital", "of"]

    # In 1 target forward pass, we generated 3 accepted tokens + 1 target correction token = 4 tokens total
    total_tokens = count_1 + 1
    target_passes = 1
    speedup = simulator.calculate_speedup_ratio(total_tokens, target_passes)
    print(f"Speedup Ratio: {speedup:.2f}x")
    assert speedup == 4.0

    # Case 2: Target model agrees on all draft tokens
    target_probs_2 = [0.85, 0.75, 0.95, 0.70]
    accepted_2, count_2 = simulator.verify_speculative_tokens(draft_tokens, draft_probs, target_probs_2)
    assert count_2 == 4
    assert accepted_2 == draft_tokens

    print("All tests passed successfully!")
