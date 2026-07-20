"""
Topic: Automatic Tool Schema Generator
Exercise: Function Inspection to OpenAI Tool Schema Converter

Problem Description:
LLM Tool Calling APIs (OpenAI, Anthropic, Gemini) require function tools to be defined in 
strict JSON Schema format. Writing these manually is repetitive and prone to drift.

Implement an `AutoToolSchemaGenerator` class containing:
1. `python_type_to_json_type(py_type: type) -> str`:
   Maps Python types (`int`, `str`, `float`, `bool`, `list`) to JSON Schema types.
2. `generate_openai_tool_schema(func: Callable) -> dict`:
   Inspects function name, docstring, parameters, default values, and type annotations 
   to auto-generate a valid OpenAI Tool Schema.
"""

import inspect
from typing import Callable, Dict, Any, get_type_hints

class AutoToolSchemaGenerator:
    def __init__(self):
        pass

    def python_type_to_json_type(self, py_type: type) -> str:
        """
        Maps Python types to JSON schema data types.
        """
        type_map = {
            int: "integer",
            float: "number",
            str: "string",
            bool: "boolean",
            list: "array",
            dict: "object"
        }
        return type_map.get(py_type, "string")

    def generate_openai_tool_schema(self, func: Callable) -> Dict[str, Any]:
        """
        Auto-generates OpenAI Function Tool JSON Schema via reflection.
        """
        func_name = func.__name__
        docstring = inspect.getdoc(func) or f"Function {func_name}"

        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        properties = {}
        required_params = []

        for param_name, param in sig.parameters.items():
            # Skip *args or **kwargs
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

            param_type = type_hints.get(param_name, str)
            json_type = self.python_type_to_json_type(param_type)

            properties[param_name] = {
                "type": json_type,
                "description": f"Parameter {param_name}"
            }

            # If parameter has no default value, it is required
            if param.default == inspect.Parameter.empty:
                required_params.append(param_name)

        schema = {
            "type": "function",
            "function": {
                "name": func_name,
                "description": docstring,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_params
                }
            }
        }

        return schema

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Automatic Tool Schema Generator...")

    generator = AutoToolSchemaGenerator()

    # Target test function
    def calculate_shipping_cost(destination: str, weight_kg: float, is_express: bool = False) -> float:
        """Calculates shipping fees based on destination, weight in kilograms, and speed."""
        return weight_kg * 5.0

    schema = generator.generate_openai_tool_schema(calculate_shipping_cost)

    import json
    print("Generated OpenAI Tool Schema:")
    print(json.dumps(schema, indent=2))

    func_obj = schema["function"]
    assert func_obj["name"] == "calculate_shipping_cost"
    assert "Calculates shipping fees" in func_obj["description"]

    props = func_obj["parameters"]["properties"]
    assert props["destination"]["type"] == "string"
    assert props["weight_kg"]["type"] == "number"
    assert props["is_express"]["type"] == "boolean"

    # destination and weight_kg are required; is_express has default False so it is optional
    required = func_obj["parameters"]["required"]
    assert "destination" in required
    assert "weight_kg" in required
    assert "is_express" not in required

    print("All tests passed successfully!")
