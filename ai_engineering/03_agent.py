"""
Topic: Agent
Exercise: Autonomous ReAct Agent Loop

Problem Description:
An AI Agent uses a "Reasoning and Acting" (ReAct) loop to solve complex tasks. 
Given a prompt, the agent breaks down the problem, plans steps, invokes tools to observe results, 
and reasons through subsequent steps until reaching a final answer.

Implement an `Agent` class containing:
1. **Tools Registry**: A set of helper functions (e.g., `add`, `multiply`).
2. **Reasoning Loop**: Loop representing Thought, Action, Observation.
3. **Planning & Parsers**: Extract target tool name and arguments from a string like 
   `Action: add(5, 3)` and feed the output of tool execution back as an observation.
"""

from typing import Dict, Callable, Tuple, Optional

class ReActAgent:
    def __init__(self):
        self.tools: Dict[str, Callable] = {
            "add": self._add,
            "multiply": self._multiply,
            "subtract": self._subtract
        }
        self.history = []

    def _add(self, x: float, y: float) -> float:
        return x + y

    def _multiply(self, x: float, y: float) -> float:
        return x * y

    def _subtract(self, x: float, y: float) -> float:
        return x - y

    def parse_action(self, agent_output: str) -> Optional[Tuple[str, list]]:
        """
        Parses an agent output string looking for 'Action: tool_name(arg1, arg2)'.
        Returns a tuple of (tool_name, arguments_list) or None if no action is found.
        """
        if "Action:" in agent_output:
            try:
                action_str = agent_output.split("Action:")[1].strip()
                tool_name = action_str.split("(")[0].strip()
                args_str = action_str.split("(")[1].split(")")[0]
                args = [float(arg.strip()) for arg in args_str.split(",") if arg.strip()]
                return tool_name, args
            except Exception:
                return None
        return None

    def run(self, task: str, mock_llm_steps: list) -> str:
        """
        Simulates the execution of the agent loop using a predefined list of 'mock_llm_steps'
        representing the reasoning/action tokens returned by the LLM at each turn.
        """
        self.history = []
        step_idx = 0
        
        print(f"Agent Task: {task}")
        
        while step_idx < len(mock_llm_steps):
            # 1. Get thought/action suggestion from mock LLM response
            response = mock_llm_steps[step_idx]
            self.history.append(f"Agent: {response}")
            print(f"Agent Output:\n{response}")
            
            # Check if this output is a final answer
            if "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()
                
            # 2. Parse and execute action if present
            action = self.parse_action(response)
            if action:
                tool_name, args = action
                if tool_name in self.tools:
                    # Execute tool
                    try:
                        observation = self.tools[tool_name](*args)
                        obs_str = f"Observation: {observation}"
                        self.history.append(obs_str)
                        print(f"Execution -> {obs_str}\n")
                    except Exception as e:
                        obs_str = f"Observation: Error executing tool: {e}"
                        self.history.append(obs_str)
                        print(f"Execution -> {obs_str}\n")
                else:
                    obs_str = f"Observation: Tool '{tool_name}' not found."
                    self.history.append(obs_str)
                    print(f"Execution -> {obs_str}\n")
            else:
                print("No action taken.\n")
                
            step_idx += 1
            
        return "Failed to find final answer."

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for ReAct Agent...")
    
    agent = ReActAgent()
    
    # Task: Add 5 and 3, then multiply the result by 10.
    task = "Solve (5 + 3) * 10"
    
    # Mock LLM outputs representing the agent's chain of thought loop.
    # It first decides to add, gets the observation 8, then decides to multiply.
    mock_steps = [
        "Thought: I need to calculate the sum of 5 and 3 first.\nAction: add(5, 3)",
        "Thought: Now I have the sum (8). I need to multiply it by 10.\nAction: multiply(8, 10)",
        "Thought: I have computed the final product (80).\nFinal Answer: 80"
    ]
    
    final_answer = agent.run(task, mock_steps)
    print(f"Final Answer returned: {final_answer}")
    assert final_answer == "80", "Agent failed to compute correct answer!"
    
    # Verify action parsing correctness
    parsed = agent.parse_action("Action: multiply(10.5, 2)")
    assert parsed == ("multiply", [10.5, 2.0])
    
    parsed_bad = agent.parse_action("Thought: I am done.")
    assert parsed_bad is None
    
    print("All tests passed successfully!")
