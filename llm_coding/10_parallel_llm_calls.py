"""
Topic: Parallel LLM Calls
Exercise: Concurrent LLM Batch Processor

Problem Description:
Processing a large list of prompts sequentially is slow. We can use python concurrency 
(thread pools) to query APIs in parallel. However, parallel execution must handle:
1. Max concurrency limits (throttling number of simultaneous connections).
2. Individual request failures (a single failed request should not abort the entire batch).
3. Maintaining the correct mapping of prompts to responses in the output list.

Implement a function `batch_process_prompts` that:
- Receives a list of `prompts` (strings) and a `query_fn` (a callable simulating the LLM API call).
- Executes `query_fn` for each prompt in parallel using `ThreadPoolExecutor`.
- Limits the number of concurrent threads to `max_concurrency`.
- Catches any exception raised by `query_fn`. In case of error, returns a default error string 
  (e.g., `"ERROR: <exception_message>"`).
- Returns the list of responses in the *exact same order* as the input prompts.

Interface:
- `batch_process_prompts(prompts: list[str], query_fn: Callable[[str], str], max_concurrency: int = 3) -> list[str]`
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable

def batch_process_prompts(
    prompts: List[str], 
    query_fn: Callable[[str], str], 
    max_concurrency: int = 3
) -> List[str]:
    """
    Executes query_fn on each prompt in prompts in parallel, capping concurrency at max_concurrency,
    and returns results in the original order.
    """
    # We will use ThreadPoolExecutor to run queries in parallel.
    # To maintain the original order, we can map each future back to its index.
    results = [None] * len(prompts)
    
    with ThreadPoolExecutor(max_workers=max_concurrency) as executor:
        # Submit all tasks and map futures to their original index
        future_to_index = {
            executor.submit(query_fn, prompt): idx 
            for idx, prompt in enumerate(prompts)
        }
        
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                # Retrieve the result of the future
                results[idx] = future.result()
            except Exception as e:
                # Capture exception message in place without crashing the batch
                results[idx] = f"ERROR: {str(e)}"
                
    return results

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Parallel LLM Processor...")
    
    # Mock LLM query function
    def mock_query(prompt: str) -> str:
        # Simulate slight latency
        time.sleep(0.05)
        if "fail" in prompt.lower():
            raise RuntimeWarning("API Call Failed")
        return f"Response to {prompt}"
        
    prompts = [
        "Prompt A",
        "Prompt B (fail)",
        "Prompt C",
        "Prompt D",
        "Prompt E (fail)"
    ]
    
    start_time = time.time()
    responses = batch_process_prompts(prompts, mock_query, max_concurrency=3)
    duration = time.time() - start_time
    
    print(f"Responses: {responses}")
    print(f"Time taken: {duration:.4f} seconds")
    
    # Assertions
    assert len(responses) == len(prompts)
    assert responses[0] == "Response to Prompt A"
    assert "ERROR:" in responses[1], "Expected error output for Prompt B"
    assert responses[2] == "Response to Prompt C"
    assert responses[3] == "Response to Prompt D"
    assert "ERROR:" in responses[4], "Expected error output for Prompt E"
    
    # Parallelism sanity check: 5 tasks with 0.05s delay using concurrency=3
    # Should take around 2 rounds of executions (~0.1s), not 0.25s (sequential)
    assert duration < 0.20, f"Execution took too long: {duration:.4f}s. Concurrency might be broken."
    
    print("All tests passed successfully!")
