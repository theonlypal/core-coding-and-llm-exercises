"""
Topic: Coding Assistant
Exercise: Local Codebase Indexer and Generator

Problem Description:
Coding assistants (like Antigravity or Copilot) need to parse local file structures, 
index functions/classes, query code symbols, and generate updates to files.

Implement a `CodingAssistant` helper class supporting:
1. `index_repository(file_map: dict[str, str]) -> dict[str, list[dict]]`:
   Parses a dictionary mapping filenames to code strings. Extracts function definitions 
   using regex patterns (e.g., matching `def function_name(args) -> return_type:`).
2. `symbol_search(query: str, index: dict) -> list[dict]`:
   Searches the function index for entries that contain the search term in their name or signature.
3. `generate_and_inject_code(target_code: str, anchor: str, new_code: str) -> str`:
   Finds an anchor line in the target code and injects the new block of code directly below it.
"""

import re
from typing import Dict, List, Any

class CodingAssistant:
    def __init__(self):
        pass

    def index_repository(self, file_map: Dict[str, str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parses a virtual repository file map and indexes all python function declarations.
        Returns a dictionary mapping filenames -> list of function details.
        """
        index = {}
        # Regex matching: def name(arguments) -> return:
        func_pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)\s*(?:->\s*([a-zA-Z0-9_\[\],\'\" ]+))?\s*:"
        
        for filepath, content in file_map.items():
            funcs = []
            lines = content.split("\n")
            for line_idx, line in enumerate(lines):
                match = re.search(func_pattern, line)
                if match:
                    func_name = match.group(1)
                    args = match.group(2).strip()
                    ret_type = match.group(3).strip() if match.group(3) else "None"
                    funcs.append({
                        "name": func_name,
                        "args": args,
                        "return_type": ret_type,
                        "line_number": line_idx + 1  # 1-indexed
                    })
            index[filepath] = funcs
            
        return index

    def symbol_search(self, query: str, index: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Searches the repository index for functions containing the query string.
        """
        matches = []
        for filepath, funcs in index.items():
            for func in funcs:
                if query.lower() in func["name"].lower():
                    matches.append({
                        "filepath": filepath,
                        "function": func
                    })
        return matches

    def generate_and_inject_code(self, target_code: str, anchor: str, new_code: str) -> str:
        """
        Injects a new block of code directly below the anchor line in target_code.
        """
        lines = target_code.split("\n")
        injected = False
        output_lines = []
        
        for line in lines:
            output_lines.append(line)
            if anchor in line and not injected:
                # Append the new code block
                output_lines.append(new_code)
                injected = True
                
        if not injected:
            raise ValueError(f"Anchor '{anchor}' not found in target code.")
            
        return "\n".join(output_lines)

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Coding Assistant...")
    
    assistant = CodingAssistant()
    
    # Mock Repository File Map
    repo = {
        "utils.py": (
            "def calculate_total(prices: list[float]) -> float:\n"
            "    return sum(prices)\n\n"
            "def format_currency(val: float) -> str:\n"
            "    return f'${val:.2f}'\n"
        ),
        "app.py": (
            "def run_server(port: int = 8080):\n"
            "    print('Server running')\n"
        )
    }
    
    # 1. Indexing
    index = assistant.index_repository(repo)
    print(f"Indexed symbols: {index}")
    assert "utils.py" in index
    assert len(index["utils.py"]) == 2
    assert index["utils.py"][0]["name"] == "calculate_total"
    assert index["utils.py"][0]["return_type"] == "float"
    assert index["app.py"][0]["line_number"] == 1
    
    # 2. Symbol Search
    results = assistant.symbol_search("currency", index)
    print(f"Search Results: {results}")
    assert len(results) == 1
    assert results[0]["filepath"] == "utils.py"
    assert results[0]["function"]["name"] == "format_currency"
    
    # 3. Code Generation & Injection
    original_code = (
        "def main():\n"
        "    # SETUP_ANCHOR\n"
        "    print('Hello World')"
    )
    anchor = "# SETUP_ANCHOR"
    new_code = "    print('Initializing database connection...')"
    
    modified_code = assistant.generate_and_inject_code(original_code, anchor, new_code)
    print(f"Modified Code:\n{modified_code}")
    assert "Initializing database connection..." in modified_code
    assert modified_code.split("\n")[2] == new_code
    
    print("All tests passed successfully!")
