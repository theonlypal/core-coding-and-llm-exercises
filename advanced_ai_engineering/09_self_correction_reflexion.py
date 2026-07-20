"""
Topic: Self-Correction & Reflexion Loop
Exercise: Automated Code Self-Correction Engine

Problem Description:
When LLMs generate code, execution errors or failed unit tests often occur. 
Reflexion loops execute generated code against unit tests, catch stack traces, 
and feed the error logs back to the LLM to self-correct until all tests pass.

Implement a `SelfCorrectionLoop` class containing:
1. `execute_code_with_tests(code: str, test_code: str) -> tuple[bool, str]`:
   Executes `code` + `test_code` in a dynamic namespace. Returns `(True, "Success")` 
   if tests pass, or `(False, error_traceback)` if an exception occurs.
2. `run_reflexion_loop(task_prompt: str, test_code: str, mock_llm_generator: Callable[[str], str], max_retries: int = 3) -> tuple[str, bool, int]`:
   Loops through generation, execution, error feedback, and re-prompting until tests pass 
   or retries are exhausted.
"""

import sys
import traceback
from typing import Tuple, Callable, Dict, Any

class SelfCorrectionLoop:
    def __init__(self):
        pass

    def execute_code_with_tests(self, code: str, test_code: str) -> Tuple[bool, str]:
        """
        Executes code combined with test_code in an isolated namespace dictionary.
        Returns (success_flag, output_or_error_message).
        """
        combined_code = f"{code}\n\n{test_code}"
        namespace: Dict[str, Any] = {}
        
        try:
            exec(combined_code, namespace)
            return True, "All unit tests passed successfully."
        except Exception as e:
            # Capture error details and traceback
            tb_str = "".join(traceback.format_exception(*sys.exc_info()))
            return False, f"{type(e).__name__}: {str(e)}\nTraceback:\n{tb_str}"

    def run_reflexion_loop(
        self, 
        task_prompt: str, 
        test_code: str, 
        mock_llm_generator: Callable[[str], str], 
        max_retries: int = 3
    ) -> Tuple[str, bool, int]:
        """
        Executes self-correction generation loop.
        Returns (final_code, success_flag, total_attempts).
        """
        current_prompt = f"Task: {task_prompt}\nWrite valid Python code."
        attempts = 0
        
        while attempts <= max_retries:
            attempts += 1
            # 1. Generate code from LLM
            generated_code = mock_llm_generator(current_prompt)
            print(f"[Attempt {attempts}] Generated Code:\n{generated_code}")
            
            # 2. Test code execution
            success, message = self.execute_code_with_tests(generated_code, test_code)
            
            if success:
                print(f"[Attempt {attempts}] Success: {message}\n")
                return generated_code, True, attempts
            else:
                print(f"[Attempt {attempts}] Failed with error:\n{message}\n")
                # 3. Formulate feedback prompt for self-correction
                current_prompt = (
                    f"Task: {task_prompt}\n"
                    f"Your previous code:\n```python\n{generated_code}\n```\n\n"
                    f"Failed with error:\n{message}\n\n"
                    "Fix the bug and provide the corrected Python code:"
                )
                
        return generated_code, False, attempts

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Self-Correction Reflexion Loop...")
    
    def run_tests():
        correction_engine = SelfCorrectionLoop()
        
        task_prompt = "Write a function `divide(a, b)` that divides a by b."
        test_code = "assert divide(10, 2) == 5\nassert divide(9, 3) == 3"
        
        attempts_counter = 0
        
        # Mock LLM generator that deliberately fails on first attempt with a SyntaxError/NameError,
        # then self-corrects on the second attempt after receiving feedback
        def mock_llm(prompt: str) -> str:
            nonlocal attempts_counter
            attempts_counter += 1
            if attempts_counter == 1:
                # Buggy code: misnamed function 'div' instead of 'divide'
                return "def div(a, b):\n    return a / b"
            else:
                # Corrected code
                return "def divide(a, b):\n    return a / b"
                
        final_code, success, total_attempts = correction_engine.run_reflexion_loop(
            task_prompt, test_code, mock_llm, max_retries=3
        )
        
        print(f"Final Execution Success: {success} in {total_attempts} attempts.")
        assert success is True
        assert total_attempts == 2
        assert "def divide" in final_code

    run_tests()
    print("All tests passed successfully!")
