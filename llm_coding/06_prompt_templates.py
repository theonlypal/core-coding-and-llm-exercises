"""
Topic: Prompt Templates
Exercise: Prompt Template Engine

Problem Description:
Prompt engineering is fundamental to working with LLMs. Prompt templates allow dynamically
injecting variables into text prompts while validating inputs.

Implement a `PromptTemplate` class that:
1. Receives a template string (e.g., "Hello {name}, your task is {task}.").
2. Extracts variables inside `{var_name}` automatically.
3. Supports setting default values for variables.
4. `format(**kwargs) -> str`: Interpolates values. Raises a `ValueError` if a required variable
   (without a default) is missing from `kwargs`.
5. `to_chat_messages(role: str, **kwargs) -> dict`: Returns a chat-completion formatted dict
   like `{"role": role, "content": formatted_prompt}`.
"""

import re
from typing import Dict, Set

class PromptTemplate:
    def __init__(self, template: str, defaults: Dict[str, str] = None):
        self.template = template
        self.defaults = defaults or {}
        
        # Extract variables enclosed in single braces {variable_name}
        # Avoid matching double braces {{escaped}} by using a regex lookahead/lookbehind
        # A simple way is to find all {var} and ignore {{ or }}
        self.variables: Set[str] = self._extract_variables(template)

    def _extract_variables(self, template: str) -> Set[str]:
        # Matches patterns like {variable_name} but not {{variable_name}}
        # We can find matches of { followed by alphanumeric/underscore and }
        # And filter out any that are part of double braces
        pattern = r"(?<!\{)\{([a-zA-Z0-9_]+)\}(?!\})"
        return set(re.findall(pattern, template))

    def format(self, **kwargs) -> str:
        """
        Interpolates variables and returns the formatted prompt string.
        Raises ValueError if any required variables are missing.
        """
        # Combine provided args with defaults
        vars_to_use = {**self.defaults, **kwargs}
        
        # Check for missing variables
        missing_vars = self.variables - set(vars_to_use.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables for template: {missing_vars}")
            
        # Perform interpolation.
        # We can replace single braces, but keep double braces as single braces (standard python formatting)
        # Python's str.format does this automatically! But we must make sure we only pass keys that are in the template
        # to avoid KeyErrors or formatting issues.
        # To make it robust:
        try:
            return self.template.format(**vars_to_use)
        except KeyError as e:
            raise ValueError(f"KeyError during formatting: {e}")

    def to_chat_messages(self, role: str, **kwargs) -> dict:
        """
        Formats the template and returns a dictionary representation suitable for Chat APIs.
        """
        formatted = self.format(**kwargs)
        return {
            "role": role,
            "content": formatted
        }

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Prompt Template Engine...")
    
    # Simple template
    template_str = "You are a helpful AI assistant specialized in {field}. Answer the user's question: {question}"
    
    # Initialize with default value for 'field'
    pt = PromptTemplate(template_str, defaults={"field": "Python programming"})
    
    # 1. Format with all variables (overriding default)
    formatted_1 = pt.format(field="Machine Learning", question="What is backpropagation?")
    expected_1 = "You are a helpful AI assistant specialized in Machine Learning. Answer the user's question: What is backpropagation?"
    assert formatted_1 == expected_1, f"Expected '{expected_1}', got '{formatted_1}'"
    
    # 2. Format using default
    formatted_2 = pt.format(question="What is a list comprehension?")
    expected_2 = "You are a helpful AI assistant specialized in Python programming. Answer the user's question: What is a list comprehension?"
    assert formatted_2 == expected_2, f"Expected '{expected_2}', got '{formatted_2}'"
    
    # 3. Format with missing required variable
    try:
        pt.format()  # missing question
        assert False, "Should raise ValueError for missing 'question'"
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    # 4. Chat messages format
    chat_msg = pt.to_chat_messages(role="system", question="What is decorators?")
    assert chat_msg["role"] == "system"
    assert "specialized in Python programming" in chat_msg["content"]
    
    print("All tests passed successfully!")
