"""
Topic: Multi-Agent DAG Orchestrator
Exercise: Workflow Graph Execution Engine for Specialized Agents

Problem Description:
Complex AI applications use specialized agents connected in a Directed Acyclic Graph (DAG).
For example: Researcher Agent -> Writer Agent -> Fact Checker Agent.

Implement a `MultiAgentDAGRunner` class containing:
1. `add_agent(agent_id: str, handler: Callable[[dict], dict], dependencies: list[str]) -> None`:
   Registers an agent node with its execution handler and upstream dependency IDs.
2. `topological_sort() -> list[str]`:
   Orders agent execution sequence so all upstream dependencies run before downstream agents.
3. `run(initial_state: dict) -> dict`:
   Executes agents in topological order, merging each agent's dict output into the global state.
"""

from collections import deque, defaultdict
from typing import Dict, List, Callable, Any

class MultiAgentDAGRunner:
    def __init__(self):
        # agent_id -> (handler, dependencies_list)
        self.agents: Dict[str, Tuple[Callable[[dict], dict], List[str]]] = {}

    def add_agent(self, agent_id: str, handler: Callable[[dict], dict], dependencies: List[str] = None) -> None:
        deps = dependencies or []
        self.agents[agent_id] = (handler, deps)

    def topological_sort(self) -> List[str]:
        """
        Computes topological order using Kahn's algorithm (indegree counting).
        """
        indegree = {agent_id: 0 for agent_id in self.agents}
        graph = defaultdict(list)

        for agent_id, (_, deps) in self.agents.items():
            for dep in deps:
                if dep not in self.agents:
                    raise ValueError(f"Dependency '{dep}' for agent '{agent_id}' is not registered!")
                graph[dep].append(agent_id)
                indegree[agent_id] += 1

        queue = deque([agent_id for agent_id, deg in indegree.items() if deg == 0])
        sorted_order = []

        while queue:
            node = queue.popleft()
            sorted_order.append(node)
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_order) != len(self.agents):
            raise ValueError("Cycle detected in Multi-Agent DAG!")

        return sorted_order

    def run(self, initial_state: dict) -> dict:
        """
        Executes agents in topological order, updating global state.
        """
        order = self.topological_sort()
        state = initial_state.copy()

        print(f"Executing DAG Order: {' -> '.join(order)}")

        for agent_id in order:
            handler, deps = self.agents[agent_id]
            # Execute agent handler with current shared state
            output = handler(state)
            if isinstance(output, dict):
                state.update(output)
            print(f"Completed Agent '{agent_id}'. State Keys: {list(state.keys())}")

        return state

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Multi-Agent DAG Orchestrator...")

    runner = MultiAgentDAGRunner()

    # Agent 1: Researcher
    def research_agent(state: dict) -> dict:
        topic = state.get("topic", "AI")
        return {"raw_data": f"Research data about {topic}."}

    # Agent 2: Writer (Depends on Researcher)
    def writer_agent(state: dict) -> dict:
        raw = state.get("raw_data", "")
        return {"draft": f"Draft article based on: {raw}"}

    # Agent 3: Evaluator (Depends on Writer)
    def evaluator_agent(state: dict) -> dict:
        draft = state.get("draft", "")
        return {"final_approved_article": f"{draft} [APPROVED]"}

    runner.add_agent("evaluator", evaluator_agent, dependencies=["writer"])
    runner.add_agent("researcher", research_agent, dependencies=[])
    runner.add_agent("writer", writer_agent, dependencies=["researcher"])

    # Verify topological order: researcher -> writer -> evaluator
    order = runner.topological_sort()
    assert order == ["researcher", "writer", "evaluator"]

    # Run DAG execution
    final_state = runner.run({"topic": "Quantum Computing"})
    print(f"Final State Article: '{final_state.get('final_approved_article')}'")

    assert "Quantum Computing" in final_state["final_approved_article"]
    assert "[APPROVED]" in final_state["final_approved_article"]

    print("All tests passed successfully!")
