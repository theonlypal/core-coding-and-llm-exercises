"""
Topic: Retry with Exponential Backoff
Exercise: Retry Decorator with Exponential Backoff and Jitter

Problem Description:
Network issues and API rate limit errors (like HTTP 429) are common. Standard retries
can overwhelm a service if many clients retry at the exact same intervals (thundering herd).
Exponential backoff with jitter multiplies the delay on each failure and adds a random
variance (jitter) to distribute retry times.

Implement a decorator `@retry_with_backoff` that wraps a function.
Parameters:
- `max_retries`: Maximum number of retry attempts before giving up.
- `initial_delay`: Base sleep duration in seconds before first retry.
- `backoff_factor`: Multiplier applied to delay on each subsequent retry.
- `jitter`: Boolean. If true, randomizes the delay uniformly between 0 and the current delay.
- `exceptions_to_retry`: A tuple of exception classes that trigger a retry.

Formula for sleep time:
- Attempt 1: delay = initial_delay
- Attempt 2: delay = initial_delay * backoff_factor
- Attempt 3: delay = initial_delay * backoff_factor^2
If `jitter` is True, actual sleep time is random.uniform(0, current_delay).
"""

import random
import time
import functools
from typing import Type, Tuple, Union, Callable, Any

def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 0.1,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions_to_retry: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception
) -> Callable:
    """
    Decorator that retries a function with exponential backoff and optional jitter.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            
            # Try function execution
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions_to_retry as e:
                    # If this is the last attempt, re-raise exception
                    if attempt == max_retries:
                        raise e
                        
                    # Calculate sleep time
                    sleep_time = delay
                    if jitter:
                        sleep_time = random.uniform(0, delay)
                        
                    print(f"[Attempt {attempt + 1}/{max_retries + 1}] Failed with {type(e).__name__}. Retrying in {sleep_time:.4f}s...")
                    time.sleep(sleep_time)
                    
                    # Update delay for next round
                    delay *= backoff_factor
                    
        return wrapper
    return decorator

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Retry with Exponential Backoff...")
    
    # Custom dummy exception
    class RateLimitError(Exception):
        pass
        
    def run_tests():
        failures = 0
        
        @retry_with_backoff(
            max_retries=3,
            initial_delay=0.01,
            backoff_factor=2.0,
            jitter=False,  # Keep deterministic for testing delay bounds
            exceptions_to_retry=(RateLimitError,)
        )
        def call_mock_api(succeeds_at_attempt: int) -> str:
            nonlocal failures
            failures += 1
            if failures < succeeds_at_attempt:
                raise RateLimitError("Rate limit exceeded")
            return "Success!"

        # Test 1: Succeeds on 3rd attempt (requires 2 retries)
        nonlocal_res = call_mock_api(succeeds_at_attempt=3)
        assert nonlocal_res == "Success!"
        assert failures == 3
        
        # Test 2: Fails after exceeding max_retries (3 retries = 4 total attempts)
        failures = 0
        try:
            call_mock_api(succeeds_at_attempt=10)
            assert False, "Should raise RateLimitError"
        except RateLimitError:
            print("Successfully caught RateLimitError after max retries.")
            assert failures == 4

    run_tests()
    print("All tests passed successfully!")
