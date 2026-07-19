"""
Topic: Rate Limiter
Exercise: Token Bucket Rate Limiter

Problem Description:
When interacting with LLM APIs, developers face strict Rate Limits (e.g., Requests Per Minute (RPM)
or Tokens Per Minute (TPM)). Exceeding these limits results in HTTP 429 errors.

Implement a thread-safe `TokenBucketRateLimiter` class that restricts request velocity.
The token bucket algorithm works as follows:
- The bucket has a maximum capacity (`capacity`).
- Tokens are added to the bucket at a constant rate (`refill_rate` tokens per second).
- Each request consumes `tokens` (defaults to 1).
- If the bucket has enough tokens, the request is allowed and tokens are deducted.
- Otherwise, the request is rejected immediately.

Interface:
- `__init__(capacity: float, refill_rate: float)`: Init capacity and refill rate.
- `allow_request(tokens: int = 1) -> bool`: Thread-safely check and consume tokens.
"""

import time
import threading

class TokenBucketRateLimiter:
    def __init__(self, capacity: float, refill_rate: float):
        """
        capacity: Maximum capacity of the token bucket.
        refill_rate: Rate at which tokens are added (tokens per second).
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        
        # Start with a full bucket
        self.tokens = capacity
        self.last_update = time.time()
        
        self.lock = threading.Lock()

    def _refill(self):
        """
        Calculates how many tokens should be added based on elapsed time.
        Must be called within lock.
        """
        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now
        
        # Add new tokens, capping at maximum capacity
        refill_amount = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + refill_amount)

    def allow_request(self, tokens: int = 1) -> bool:
        """
        Checks if the request is allowed. If allowed, consumes the tokens.
        Thread-safe.
        """
        with self.lock:
            # Refill first based on elapsed time
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
                
            return False

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Token Bucket Rate Limiter...")
    
    # Bucket capacity of 5, refilling at 2 tokens per second
    limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=2.0)
    
    # 1. Consume 5 tokens immediately (capacity allows it)
    for i in range(5):
        assert limiter.allow_request(1) is True, f"Request {i} should be allowed"
        
    # 2. 6th token should be blocked since bucket is empty
    assert limiter.allow_request(1) is False, "Request should be blocked when bucket is empty"
    
    # 3. Sleep 1 second -> bucket refills by 2 tokens
    print("Sleeping for 1 second to allow refill...")
    time.sleep(1.0)
    
    # Should allow 2 requests now
    assert limiter.allow_request(1) is True
    assert limiter.allow_request(1) is True
    assert limiter.allow_request(1) is False  # 3rd request blocked
    
    # 4. Multi-token request test
    # Refill rate is 2/sec. Wait 2 seconds -> refills 4 tokens
    time.sleep(2.0)
    assert limiter.allow_request(4) is True, "Should allow larger batch consumption"
    
    print("All tests passed successfully!")
