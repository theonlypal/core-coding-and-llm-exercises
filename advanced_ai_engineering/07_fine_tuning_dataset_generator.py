"""
Topic: Fine-Tuning Dataset Generator
Exercise: Instruction Dataset Synthesizer, Deduplicator, and Exporter

Problem Description:
Fine-tuning models requires high-quality instruction-following datasets in JSONL format:
`{"instruction": "...", "input": "...", "output": "..."}`.
Building datasets requires:
1. Schema validation (checking required non-empty string fields).
2. Semantic deduplication (removing near-duplicate instructions using vector similarity).
3. JSONL string export.

Implement a `DatasetGenerator` class containing:
1. `validate_record(record: dict) -> bool`:
   Ensures record contains valid `instruction` and `output` fields.
2. `deduplicate_records(records: list[dict], threshold: float = 0.8) -> list[dict]`:
   Filters out records whose instructions are semantically similar to an already accepted record.
3. `export_jsonl(records: list[dict]) -> str`:
   Serializes a list of valid records into a JSONL formatted string.
"""

import json
import math
import re
from typing import Dict, List, Set, Tuple

class DatasetGenerator:
    def __init__(self):
        pass

    def validate_record(self, record: dict) -> bool:
        """
        Validates schema format: instruction and output must be non-empty strings.
        """
        if not isinstance(record, dict):
            return False
        inst = record.get("instruction")
        out = record.get("output")
        if not inst or not isinstance(inst, str) or not inst.strip():
            return False
        if not out or not isinstance(out, str) or not out.strip():
            return False
        return True

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def _cosine_similarity(self, text_a: str, text_b: str) -> float:
        tokens_a = self._tokenize(text_a)
        tokens_b = self._tokenize(text_b)
        vocab = sorted(list(set(tokens_a + tokens_b)))
        if not vocab or not tokens_a or not tokens_b:
            return 0.0

        vec_a = [tokens_a.count(w) / len(tokens_a) for w in vocab]
        vec_b = [tokens_b.count(w) / len(tokens_b) for w in vocab]

        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))

        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def deduplicate_records(self, records: List[dict], threshold: float = 0.8) -> List[dict]:
        """
        Removes records if their instruction is too similar to a previously accepted record.
        """
        unique_records = []

        for rec in records:
            if not self.validate_record(rec):
                continue
                
            inst = rec["instruction"]
            is_duplicate = False
            
            for accepted in unique_records:
                sim = self._cosine_similarity(inst, accepted["instruction"])
                if sim >= threshold:
                    is_duplicate = True
                    break
                    
            if not is_duplicate:
                unique_records.append(rec)

        return unique_records

    def export_jsonl(self, records: List[dict]) -> str:
        """
        Serializes valid records into JSONL text string.
        """
        valid_records = [r for r in records if self.validate_record(r)]
        jsonl_lines = [json.dumps(r) for r in valid_records]
        return "\n".join(jsonl_lines)

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Fine-Tuning Dataset Generator...")

    generator = DatasetGenerator()

    sample_records = [
        {"instruction": "Write a python function to add numbers", "input": "", "output": "def add(a, b): return a + b"},
        {"instruction": "Write a python script to sum numbers", "input": "", "output": "def sum(x, y): return x + y"}, # duplicate
        {"instruction": "Explain quantum physics to a 5 year old", "input": "", "output": "Quantum physics is about tiny building blocks..."}, # unique
        {"instruction": "", "output": "invalid record"} # invalid schema
    ]

    # 1. Validation Test
    assert generator.validate_record(sample_records[0]) is True
    assert generator.validate_record(sample_records[3]) is False

    # 2. Deduplication Test (should remove record index 1 and 3, leaving 2 unique records)
    deduped = generator.deduplicate_records(sample_records, threshold=0.6)
    print(f"Original Records: {len(sample_records)}, Deduped: {len(deduped)}")
    assert len(deduped) == 2

    # 3. Export JSONL Test
    jsonl_output = generator.export_jsonl(deduped)
    print("Exported JSONL:")
    print(jsonl_output)

    lines = jsonl_output.split("\n")
    assert len(lines) == 2
    parsed_line_1 = json.loads(lines[0])
    assert "instruction" in parsed_line_1

    print("All tests passed successfully!")
