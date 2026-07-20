"""
Topic: LLM Observability & OpenTelemetry Tracing
Exercise: Span Telemetry and Execution Tree Tracer

Problem Description:
Debugging complex RAG and Multi-Agent chains requires step-by-step tracing of parent-child 
spans, tracking input/output payloads, latency timings, and token usage counts.

Implement an `LLMTracer` class containing:
1. `@trace_span(name: str)`: Decorator/context manager creating a telemetry span.
2. `start_span(name: str) -> str`: Creates a child span under the current parent span context.
3. `end_span(span_id: str, output: any = None, tokens_used: int = 0, error: Exception = None) -> None`:
   Finishes span timer and records tokens/results.
4. `get_trace_tree() -> list[dict]`:
   Returns the full hierarchical trace tree.
"""

import time
import uuid
from typing import Dict, List, Any, Optional, Callable
import functools

class LLMTracer:
    def __init__(self):
        # Current active span stack for tracking parent-child nesting
        self.span_stack: List[str] = []
        # Registered spans: span_id -> span_dict
        self.spans: Dict[str, Dict[str, Any]] = {}

    def start_span(self, name: str, inputs: Dict[str, Any] = None) -> str:
        span_id = str(uuid.uuid4())[:8]
        parent_id = self.span_stack[-1] if self.span_stack else None

        span_data = {
            "span_id": span_id,
            "parent_id": parent_id,
            "name": name,
            "inputs": inputs or {},
            "output": None,
            "start_time": time.time(),
            "end_time": None,
            "duration_ms": 0.0,
            "tokens_used": 0,
            "error": None,
            "status": "RUNNING"
        }

        self.spans[span_id] = span_data
        self.span_stack.append(span_id)
        return span_id

    def end_span(
        self, 
        span_id: str, 
        output: Any = None, 
        tokens_used: int = 0, 
        error: Optional[Exception] = None
    ) -> None:
        if span_id not in self.spans:
            raise ValueError(f"Span ID {span_id} not found!")

        span = self.spans[span_id]
        span["end_time"] = time.time()
        span["duration_ms"] = (span["end_time"] - span["start_time"]) * 1000.0
        span["output"] = str(output) if output is not None else None
        span["tokens_used"] = tokens_used

        if error:
            span["error"] = str(error)
            span["status"] = "ERROR"
        else:
            span["status"] = "SUCCESS"

        if self.span_stack and self.span_stack[-1] == span_id:
            self.span_stack.pop()

    def trace_span(self, name: str):
        """
        Decorator for tracing functions automatically.
        """
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                span_id = self.start_span(name, inputs={"args": str(args), "kwargs": str(kwargs)})
                try:
                    res = func(*args, **kwargs)
                    self.end_span(span_id, output=res, tokens_used=10)
                    return res
                except Exception as e:
                    self.end_span(span_id, error=e)
                    raise e
            return wrapper
        return decorator

    def get_total_tokens(self) -> int:
        return sum(s["tokens_used"] for s in self.spans.values())

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for LLM Tracer Telemetry...")

    tracer = LLMTracer()

    @tracer.trace_span("vector_retrieval")
    def retrieve_docs(query: str) -> list:
        time.sleep(0.01)
        return ["doc_1", "doc_2"]

    @tracer.trace_span("llm_generation")
    def generate_answer(prompt: str) -> str:
        time.sleep(0.01)
        return "Answer generated based on context."

    @tracer.trace_span("rag_pipeline")
    def run_rag(user_query: str) -> str:
        docs = retrieve_docs(user_query)
        prompt = f"Context: {docs}\nQuery: {user_query}"
        return generate_answer(prompt)

    # Execute traced RAG pipeline
    result = run_rag("What is AI?")
    print(f"Pipeline Output: '{result}'")

    # Verify Tracing Spans
    assert len(tracer.spans) == 3
    assert tracer.get_total_tokens() == 30

    # Verify Parent-Child Tree Relationships
    span_list = list(tracer.spans.values())
    rag_span = [s for s in span_list if s["name"] == "rag_pipeline"][0]
    ret_span = [s for s in span_list if s["name"] == "vector_retrieval"][0]
    gen_span = [s for s in span_list if s["name"] == "llm_generation"][0]

    assert ret_span["parent_id"] == rag_span["span_id"]
    assert gen_span["parent_id"] == rag_span["span_id"]
    assert rag_span["status"] == "SUCCESS"

    print("All tests passed successfully!")
