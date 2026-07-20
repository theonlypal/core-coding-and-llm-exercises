"""
Topic: Guided Decoding Logit Masker
Exercise: Constrained Logit Masking using Finite State Machines

Problem Description:
Generative models can produce invalid JSON or broken syntax. Guided / constrained decoding 
modifies raw model logits before sampling by setting invalid token logits to -inf, 
guaranteeing 100% syntactically valid outputs.

Implement a `GuidedDecodingMasker` class containing:
1. `get_valid_tokens(state: str) -> list[str]`:
   Returns allowed tokens for state: `"START"`, `"KEY"`, `"COLON"`, `"VALUE"`, or `"END"`.
2. `mask_logits(vocab: list[str], logits: list[float], allowed_tokens: list[str]) -> list[float]`:
   Sets logits of tokens NOT in `allowed_tokens` to `-float('inf')`.
3. `sample_next_token(vocab: list[str], masked_logits: list[float]) -> str`:
   Selects the highest logit token (greedy argmax).
"""

import math
from typing import List, Dict, Set

class GuidedDecodingMasker:
    def __init__(self):
        # FSM State transition map: state -> allowed token types / literals
        self.state_transitions = {
            "START": ["{"],
            "KEY": ['"name"', '"age"'],
            "COLON": [":"],
            "VALUE": ['"Alice"', "25"],
            "END": ["}"]
        }

    def get_allowed_tokens(self, current_state: str) -> List[str]:
        return self.state_transitions.get(current_state, [])

    def mask_logits(self, vocab: List[str], logits: List[float], allowed_tokens: List[str]) -> List[float]:
        """
        Masks logits of tokens not in allowed_tokens by setting them to -inf.
        """
        allowed_set = set(allowed_tokens)
        masked = []
        for token, logit in zip(vocab, logits):
            if token in allowed_set:
                masked.append(logit)
            else:
                masked.append(-float("inf"))
        return masked

    def sample_next_token(self, vocab: List[str], masked_logits: List[float]) -> str:
        """
        Selects the token with the highest logit value (argmax).
        """
        best_token = None
        best_logit = -float("inf")
        for token, logit in zip(vocab, masked_logits):
            if logit > best_logit:
                best_logit = logit
                best_token = token
        if best_token is None:
            raise ValueError("All logits are masked to -inf! No valid tokens available.")
        return best_token

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Guided Decoding Logit Masker...")

    masker = GuidedDecodingMasker()
    vocab = ["{", "}", '"name"', '"age"', ":", '"Alice"', "25", "invalid_token"]

    # Raw model unconstrained logits (where 'invalid_token' has highest score 10.0)
    raw_logits = [2.0, 1.0, 3.0, 2.5, 4.0, 5.0, 1.5, 10.0]

    # Step 1: State is "START", allowed is ["{"]
    allowed = masker.get_allowed_tokens("START")
    masked_1 = masker.mask_logits(vocab, raw_logits, allowed)
    token_1 = masker.sample_next_token(vocab, masked_1)
    print(f"State START -> Sampled: '{token_1}'")
    assert token_1 == "{"

    # Step 2: State is "KEY", allowed is ['"name"', '"age"']
    allowed_2 = masker.get_allowed_tokens("KEY")
    masked_2 = masker.mask_logits(vocab, raw_logits, allowed_2)
    token_2 = masker.sample_next_token(vocab, masked_2)
    print(f"State KEY -> Sampled: '{token_2}'")
    assert token_2 == '"name"'  # logit 3.0 > logit 2.5 ('"age"')

    # Verify invalid_token was masked
    invalid_idx = vocab.index("invalid_token")
    assert masked_2[invalid_idx] == -float("inf")

    print("All tests passed successfully!")
