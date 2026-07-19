"""
Topic: JSON Schema Validation
Exercise: Structured Output Validator

Problem Description:
LLMs are frequently prompted to return structured outputs (like JSON). However, LLM outputs
are strings and might be malformed, contain extra/missing keys, or have incorrect types.
A validator parses the JSON string and checks it against a schema to ensure type safety.

Implement a `JSONSchemaValidator` class.
The schema is defined as a dictionary mapping keys to their validation requirements. E.g.:
```python
schema = {
    "name": {"type": "string", "required": True},
    "age": {"type": "integer", "required": False},
    "score": {"type": "float", "required": True},
    "is_active": {"type": "boolean", "required": True},
    "tags": {"type": "array", "item_type": "string", "required": False}
}
```

Methods to implement:
1. `validate(json_str: str) -> dict`:
   - Parses the JSON string.
   - Raises `SchemaValidationError` (custom exception) if the JSON is syntactically invalid.
   - Validates each field. Raises `SchemaValidationError` with details if:
     - A required key is missing.
     - A key has the incorrect type.
     - An array has items with the incorrect type.
   - Performs automatic casting: e.g., if a field type is `float` but value is `42`, cast to `42.0`.
     If field type is `integer` but value is `"42"`, cast it to `42` (if possible).
   - Returns the clean, validated, and type-cast dictionary.
"""

import json
from typing import Any, Dict

class SchemaValidationError(Exception):
    """Custom exception raised when JSON validation fails."""
    pass

class JSONSchemaValidator:
    def __init__(self, schema: Dict[str, dict]):
        """
        schema: A dictionary where keys are field names, and values are dicts containing:
                - 'type': 'string', 'integer', 'float', 'boolean', 'array'
                - 'required': bool
                - 'item_type': (optional, for 'array' type) e.g. 'string', 'integer'
        """
        self.schema = schema

    def validate(self, json_str: str) -> Dict[str, Any]:
        """
        Parses a JSON string, validates it against the schema, type-casts when possible,
        and returns the validated dictionary.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise SchemaValidationError(f"Invalid JSON format: {e}")
            
        if not isinstance(data, dict):
            raise SchemaValidationError("Root of JSON must be an object.")
            
        validated_data = {}
        
        for field, rules in self.schema.items():
            field_type = rules.get("type")
            required = rules.get("required", False)
            
            # Check for missing field
            if field not in data:
                if required:
                    raise SchemaValidationError(f"Missing required field: '{field}'")
                continue
                
            val = data[field]
            
            # Handle null values (None in Python)
            if val is None:
                if required:
                    raise SchemaValidationError(f"Field '{field}' is required and cannot be null")
                validated_data[field] = None
                continue
                
            # Perform validation and type casting
            try:
                if field_type == "string":
                    if not isinstance(val, str):
                        # Force cast to string
                        val = str(val)
                    validated_data[field] = val
                    
                elif field_type == "integer":
                    if not isinstance(val, int) or isinstance(val, bool): # in Python, isinstance(True, int) is True!
                        val = int(val)
                    validated_data[field] = val
                    
                elif field_type == "float":
                    if not isinstance(val, (int, float)) or isinstance(val, bool):
                        val = float(val)
                    validated_data[field] = float(val)
                    
                elif field_type == "boolean":
                    if not isinstance(val, bool):
                        # Attempt standard casting
                        if str(val).lower() in ("true", "1"):
                            val = True
                        elif str(val).lower() in ("false", "0"):
                            val = False
                        else:
                            raise ValueError()
                    validated_data[field] = val
                    
                elif field_type == "array":
                    if not isinstance(val, list):
                        raise SchemaValidationError(f"Field '{field}' must be an array")
                        
                    item_type = rules.get("item_type")
                    validated_list = []
                    if item_type:
                        for idx, item in enumerate(val):
                            if item_type == "string":
                                validated_list.append(str(item))
                            elif item_type == "integer":
                                validated_list.append(int(item))
                            elif item_type == "float":
                                validated_list.append(float(item))
                            elif item_type == "boolean":
                                if not isinstance(item, bool):
                                    if str(item).lower() in ("true", "1"):
                                        validated_list.append(True)
                                    elif str(item).lower() in ("false", "0"):
                                        validated_list.append(False)
                                    else:
                                        raise ValueError()
                                else:
                                    validated_list.append(item)
                            else:
                                validated_list.append(item)
                    else:
                        validated_list = val
                    validated_data[field] = validated_list
                else:
                    validated_data[field] = val
                    
            except (ValueError, TypeError):
                raise SchemaValidationError(f"Type mismatch for field '{field}': expected {field_type}, got {type(val).__name__}")
                
        return validated_data

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for JSON Schema Validator...")
    
    schema = {
        "name": {"type": "string", "required": True},
        "age": {"type": "integer", "required": False},
        "score": {"type": "float", "required": True},
        "is_active": {"type": "boolean", "required": True},
        "tags": {"type": "array", "item_type": "string", "required": False}
    }
    
    validator = JSONSchemaValidator(schema)
    
    # 1. Valid JSON string with type-casting required for 'score' (int -> float) and 'age' (str -> int)
    input_json = '{"name": "Alice", "age": "28", "score": 95, "is_active": true, "tags": ["AI", "developer"]}'
    res = validator.validate(input_json)
    print(f"Validated dict: {res}")
    
    assert res["name"] == "Alice"
    assert res["age"] == 28
    assert isinstance(res["score"], float) and res["score"] == 95.0
    assert res["is_active"] is True
    assert res["tags"] == ["AI", "developer"]
    
    # 2. Missing required field 'score'
    bad_json_1 = '{"name": "Bob", "is_active": false}'
    try:
        validator.validate(bad_json_1)
        assert False, "Should raise SchemaValidationError due to missing required field 'score'"
    except SchemaValidationError as e:
        print(f"Caught expected error: {e}")
        assert "Missing required field: 'score'" in str(e)
        
    # 3. Invalid JSON syntax
    bad_json_2 = '{"name": "Charlie", "age": 30, }'  # trailing comma is invalid in JSON standard
    try:
        validator.validate(bad_json_2)
        assert False, "Should raise SchemaValidationError due to syntax error"
    except SchemaValidationError as e:
        print(f"Caught expected error: {e}")
        
    print("All tests passed successfully!")
