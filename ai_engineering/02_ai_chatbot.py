"""
Topic: AI Chatbot
Exercise: End-to-End Chatbot Loop

Problem Description:
An AI Chatbot needs conversation memory, streaming capabilities, tool calling, and 
structured output formatting.

Implement a `ChatbotController` class containing:
1. **Conversation Memory**: Maintain a history of messages (`role` and `content`). Support pruning 
   to the last `max_messages` messages.
2. **Tool Calling**: Detect if a response requests a tool call (e.g., `CALL_TOOL: <tool_name>(<arg>)`), 
   execute the tool locally, and add the result as a system message.
3. **Streaming Responses**: Yield chunks representing the generation stream of the final response.
4. **Structured Outputs**: Ensure the chatbot's final output can be parsed as a structured JSON object 
   containing the keys: `"message"` (str) and `"actions_taken"` (list of str).
"""

import json
import time
from typing import Dict, List, Generator, Optional

# Define local mock tools
def get_time(location: str) -> str:
    return f"The current time in {location} is 10:00 PM."

def calculate(expression: str) -> str:
    try:
        # A safe eval for simple math expressions
        clean_expr = "".join(c for c in expression if c.isdigit() or c in "+-*/(). ")
        return str(eval(clean_expr))
    except Exception:
        return "Error calculation"

class ChatbotController:
    def __init__(self, max_messages: int = 5):
        self.max_messages = max_messages
        self.memory: List[Dict[str, str]] = []
        self.tools = {
            "get_time": get_time,
            "calculate": calculate
        }

    def add_message(self, role: str, content: str):
        """
        Appends a message to the memory list and prunes if history size exceeds max_messages.
        """
        self.memory.append({"role": role, "content": content})
        if len(self.memory) > self.max_messages:
            self.memory = self.memory[-self.max_messages:]

    def detect_and_execute_tool(self, model_response: str) -> Optional[str]:
        """
        Detects tool calls matching the pattern 'CALL_TOOL: tool_name(arg)' and executes them.
        Returns the string result of the tool execution, or None if no tool call is detected.
        """
        if model_response.startswith("CALL_TOOL:"):
            # Parsing "CALL_TOOL: tool_name(arg)"
            try:
                parts = model_response.replace("CALL_TOOL:", "").strip().split("(")
                tool_name = parts[0].strip()
                arg = parts[1].replace(")", "").strip().strip('"').strip("'")
                
                if tool_name in self.tools:
                    result = self.tools[tool_name](arg)
                    return f"TOOL_RESULT: {result}"
            except Exception:
                return "TOOL_ERROR: Failed to parse tool execution."
        return None

    def generate_streaming_response(self, text: str) -> Generator[str, None, None]:
        """
        Yields words from text to simulate a streaming output connection.
        """
        words = text.split(" ")
        for idx, word in enumerate(words):
            chunk = word if idx == len(words) - 1 else word + " "
            yield chunk
            time.sleep(0.005)

    def format_structured_output(self, final_text: str, actions: List[str]) -> str:
        """
        Formats the chatbot response into a strict JSON string.
        """
        obj = {
            "message": final_text,
            "actions_taken": actions
        }
        return json.dumps(obj)

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for AI Chatbot...")
    
    bot = ChatbotController(max_messages=4)
    
    # 1. Test Memory Pruning
    bot.add_message("user", "Hello")
    bot.add_message("assistant", "Hi there")
    bot.add_message("user", "How's the weather?")
    bot.add_message("assistant", "Sunny")
    bot.add_message("user", "Great")
    
    # max_messages is 4, so "Hello" should be pruned out
    assert len(bot.memory) == 4
    assert bot.memory[0]["content"] == "Hi there"
    
    # 2. Test Tool Calling Execution
    tool_call_input = "CALL_TOOL: calculate(2 + 2)"
    tool_output = bot.detect_and_execute_tool(tool_call_input)
    print(f"Tool Result: {tool_output}")
    assert tool_output == "TOOL_RESULT: 4"
    
    # 3. Test Streaming Response
    test_response = "This is a stream test."
    stream_chunks = list(bot.generate_streaming_response(test_response))
    assert "".join(stream_chunks) == test_response
    assert len(stream_chunks) == 5
    
    # 4. Test Structured Outputs
    actions = ["calculate(2+2)", "format_response"]
    json_out = bot.format_structured_output("The result is 4.", actions)
    parsed = json.loads(json_out)
    assert parsed["message"] == "The result is 4."
    assert parsed["actions_taken"] == actions
    
    print("All tests passed successfully!")
