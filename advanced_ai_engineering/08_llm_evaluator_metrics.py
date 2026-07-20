"""
Topic: LLM Evaluator & Metrics
Exercise: ROUGE Metrics and LLM-as-a-Judge Evaluator

Problem Description:
Evaluating generated responses requires automated metrics and model-based scoring:
1. **ROUGE-1**: Unigram overlap precision, recall, and F1 score between candidate and reference text.
2. **ROUGE-L**: Longest Common Subsequence (LCS) overlap score.
3. **LLM-as-a-Judge**: Prompting an LLM to evaluate responses on Faithfulness (grounded in context) 
   and Answer Relevance (answering the question).

Implement an `LLMEvaluator` class containing:
1. `rouge_1(candidate: str, reference: str) -> dict[str, float]`:
   Computes ROUGE-1 precision, recall, and F1-score.
2. `rouge_l(candidate: str, reference: str) -> dict[str, float]`:
   Computes ROUGE-L based on Longest Common Subsequence length.
3. `llm_as_a_judge(query: str, context: str, response: str, mock_llm_fn: Callable[[str], str]) -> dict`:
   Prompts a judge LLM to score Faithfulness and Relevance (1-5 scale) and parses structured results.
"""

import json
import re
from typing import Dict, List, Callable, Union

class LLMEvaluator:
    def __init__(self):
        pass

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def rouge_1(self, candidate: str, reference: str) -> Dict[str, float]:
        """
        Computes ROUGE-1 unigram overlap scores.
        """
        cand_tokens = self._tokenize(candidate)
        ref_tokens = self._tokenize(reference)

        if not cand_tokens or not ref_tokens:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

        overlap = sum(min(cand_tokens.count(w), ref_tokens.count(w)) for w in set(cand_tokens))
        precision = overlap / len(cand_tokens)
        recall = overlap / len(ref_tokens)
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {"precision": precision, "recall": recall, "f1": f1}

    def _lcs_length(self, x: List[str], y: List[str]) -> int:
        m, n = len(x), len(y)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if x[i - 1] == y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    def rouge_l(self, candidate: str, reference: str) -> Dict[str, float]:
        """
        Computes ROUGE-L based on Longest Common Subsequence length.
        """
        cand_tokens = self._tokenize(candidate)
        ref_tokens = self._tokenize(reference)

        if not cand_tokens or not ref_tokens:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

        lcs = self._lcs_length(cand_tokens, ref_tokens)
        precision = lcs / len(cand_tokens)
        recall = lcs / len(ref_tokens)
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {"precision": precision, "recall": recall, "f1": f1}

    def llm_as_a_judge(
        self, 
        query: str, 
        context: str, 
        response: str, 
        mock_llm_fn: Callable[[str], str]
    ) -> Dict[str, Union[float, str]]:
        """
        Evaluates faithfulness and relevance using LLM-as-a-judge prompt.
        """
        judge_prompt = (
            "Evaluate the following response based on Query and Context.\n"
            f"Query: {query}\nContext: {context}\nResponse: {response}\n\n"
            "Return JSON format:\n"
            '{"faithfulness_score": 1-5, "relevance_score": 1-5, "reasoning": "..."}'
        )
        llm_out = mock_llm_fn(judge_prompt)
        try:
            return json.loads(llm_out)
        except Exception:
            return {"faithfulness_score": 0, "relevance_score": 0, "reasoning": "Failed to parse judge output."}

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for LLM Evaluator Metrics...")

    evaluator = LLMEvaluator()

    candidate_text = "The quick brown fox jumps over the dog"
    reference_text = "The fast brown fox jumps over a lazy dog"

    # 1. ROUGE-1 Test
    r1 = evaluator.rouge_1(candidate_text, reference_text)
    print(f"ROUGE-1: {r1}")
    assert r1["precision"] > 0.6
    assert r1["recall"] > 0.6

    # 2. ROUGE-L Test
    rl = evaluator.rouge_l(candidate_text, reference_text)
    print(f"ROUGE-L: {rl}")
    assert rl["f1"] > 0.5

    # 3. LLM-as-a-Judge Test
    def mock_judge_llm(prompt: str) -> str:
        return json.dumps({
            "faithfulness_score": 5,
            "relevance_score": 5,
            "reasoning": "Response directly answers query using provided context."
        })

    judge_res = evaluator.llm_as_a_judge("What did the fox do?", "Fox jumped.", "The fox jumped over the dog.", mock_judge_llm)
    print(f"Judge Evaluation: {judge_res}")
    assert judge_res["faithfulness_score"] == 5
    assert judge_res["relevance_score"] == 5

    print("All tests passed successfully!")
