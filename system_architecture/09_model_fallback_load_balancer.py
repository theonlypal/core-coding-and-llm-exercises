"""
Topic: Multi-Provider Load Balancer & Fallback
Exercise: Round-Robin Load Balancing and Automatic Fault-Tolerant Failover

Problem Description:
LLM API outages or rate limit bursts require resilient architecture:
1. **Load Balancing**: Distribute requests round-robin or weighted across healthy providers.
2. **Automatic Failover**: If the selected primary provider fails or times out, fail over 
   sequentially to secondary backup providers without throwing an exception to the caller.

Implement a `ModelLoadBalancer` class containing:
1. `add_provider(name: str, call_fn: Callable[[str], str], priority: int = 1) -> None`:
   Registers a provider callback with a priority rank (1 = Primary, 2 = Backup).
2. `execute_request(prompt: str) -> tuple[str, str]`:
   Attempts request on primary providers via round-robin. On error, falls back down the priority chain. 
   Returns `(response_text, provider_name_used)`.
"""

from typing import Dict, List, Callable, Tuple

class ModelLoadBalancer:
    def __init__(self):
        # priority_level -> list of (provider_name, call_fn)
        self.priority_groups: Dict[int, List[Tuple[str, Callable[[str], str]]]] = {}
        # priority_level -> round_robin index
        self.rr_index: Dict[int, int] = {}
        # provider_name -> failure count
        self.failure_counts: Dict[str, int] = {}

    def add_provider(self, name: str, call_fn: Callable[[str], str], priority: int = 1) -> None:
        if priority not in self.priority_groups:
            self.priority_groups[priority] = []
            self.rr_index[priority] = 0
        self.priority_groups[priority].append((name, call_fn))
        self.failure_counts[name] = 0

    def execute_request(self, prompt: str) -> Tuple[str, str]:
        if not self.priority_groups:
            raise RuntimeError("No model providers registered!")

        # Sort priority ranks ascending (1 is highest priority)
        sorted_priorities = sorted(list(self.priority_groups.keys()))

        for prio in sorted_priorities:
            providers = self.priority_groups[prio]
            num_providers = len(providers)
            
            # Start round-robin search within this priority level
            start_idx = self.rr_index[prio]
            
            for offset in range(num_providers):
                current_idx = (start_idx + offset) % num_providers
                name, call_fn = providers[current_idx]
                
                try:
                    # Execute call
                    response = call_fn(prompt)
                    # Update round-robin pointer for next call
                    self.rr_index[prio] = (current_idx + 1) % num_providers
                    return response, name
                except Exception as e:
                    self.failure_counts[name] += 1
                    print(f"Provider '{name}' (Priority {prio}) failed: {e}. Trying next...")
                    continue

        raise RuntimeError("All primary and backup model providers failed!")

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Model Load Balancer...")

    balancer = ModelLoadBalancer()

    # Priority 1: OpenAI Primary (Simulated failure)
    def primary_openai(prompt: str) -> str:
        raise ConnectionError("HTTP 503 Service Unavailable")

    # Priority 1: Anthropic Primary (Simulated failure)
    def primary_anthropic(prompt: str) -> str:
        raise TimeoutError("Request timed out")

    # Priority 2: Backup Local Model (Healthy)
    def backup_local(prompt: str) -> str:
        return "Local Llama 3 Backup Response"

    balancer.add_provider("OpenAI-Primary", primary_openai, priority=1)
    balancer.add_provider("Anthropic-Primary", primary_anthropic, priority=1)
    balancer.add_provider("Local-Backup", backup_local, priority=2)

    # Execute request -> Priority 1 providers fail, falls back to Priority 2 Local-Backup
    res, provider_used = balancer.execute_request("Summarize article")
    print(f"Request succeeded using provider: '{provider_used}' -> Response: '{res}'")

    assert provider_used == "Local-Backup"
    assert res == "Local-Backup Response" or "Llama 3" in res
    assert balancer.failure_counts["OpenAI-Primary"] == 1
    assert balancer.failure_counts["Anthropic-Primary"] == 1

    print("All tests passed successfully!")
