"""
Topic: Streaming Partial JSON Parser
Exercise: Incomplete JSON Token Stream Parser

Problem Description:
When streaming LLM JSON outputs, waiting for full completion before parsing delays UI feedback. 
A partial JSON parser automatically repairs and completes unclosed quotes, brackets, and braces 
as tokens arrive, returning an intermediate valid Python dictionary.

Implement a `PartialJSONParser` class containing:
1. `repair_partial_json(partial_str: str) -> str`:
   Appends closing quotes, brackets `]`, and braces `}` to turn incomplete JSON strings valid.
2. `parse(partial_str: str) -> dict`:
   Attempts standard `json.loads`. If it fails, repairs the string and returns the parsed dict.
"""

import json
from typing import Any, Dict

class PartialJSONParser:
    def __init__(self):
        pass

    def repair_partial_json(self, partial_str: str) -> str:
        """
        Repairs partial JSON by closing open quotes, brackets, and braces.
        """
        s = partial_str.strip()
        if not s:
            return "{}"

        # Track unclosed quotes and open brackets/braces
        in_string = False
        escape = False
        stack = []

        for char in s:
            if escape:
                escape = False
                continue

            if char == "\\":
                escape = True
                continue

            if char == '"':
                in_string = not in_string
            elif not in_string:
                if char in ("{", "["):
                    stack.append(char)
                elif char == "}":
                    if stack and stack[-1] == "{":
                        stack.pop()
                elif char == "]":
                    if stack and stack[-1] == "[":
                        stack.pop()

        repaired = s

        # If ended inside a string literal, close the quote
        if in_string:
            repaired += '"'

        # Handle trailing colons or commas
        repaired = repaired.rstrip()
        if repaired.endswith(":"):
            repaired += " null"
        elif repaired.endswith(","):
            repaired = repaired[:-1]

        # Close all unclosed brackets/braces in reverse order
        while stack:
            top = stack.pop()
            if top == "{":
                repaired += "}"
            elif top == "[":
                repaired += "]"

        return repaired

    def parse(self, partial_str: str) -> Dict[str, Any]:
        """
        Parses partial JSON, returning dict.
        """
        try:
            return json.loads(partial_str)
        except json.JSONDecodeError:
            repaired = self.repair_partial_json(partial_str)
            try:
                return json.loads(repaired)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse repaired JSON '{repaired}': {e}")

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Streaming Partial JSON Parser...")

    parser = PartialJSONParser()

    # 1. Partial JSON cut off inside a key string: '{"user_id": 101, "name": "Ali'
    stream_chunk_1 = '{"user_id": 101, "name": "Ali'
    parsed_1 = parser.parse(stream_chunk_1)
    print(f"Chunk 1: '{stream_chunk_1}' -> Parsed: {parsed_1}")
    assert parsed_1["user_id"] == 101
    assert parsed_1["name"] == "Ali"

    # 2. Partial JSON cut off inside an array: '{"items": ["apple", "banana", "or'
    stream_chunk_2 = '{"items": ["apple", "banana", "or'
    parsed_2 = parser.parse(stream_chunk_2)
    print(f"Chunk 2: '{stream_chunk_2}' -> Parsed: {parsed_2}")
    assert parsed_2["items"] == ["apple", "banana", "or"]

    # 3. Partial JSON cut off after a key and colon: '{"status": "active", "scores":'
    stream_chunk_3 = '{"status": "active", "scores":'
    parsed_3 = parser.parse(stream_chunk_3)
    print(f"Chunk 3: '{stream_chunk_3}' -> Parsed: {parsed_3}")
    assert parsed_3["status"] == "active"

    print("All tests passed successfully!")
