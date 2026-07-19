"""
Topic: Streaming API
Exercise: Mock LLM Streaming API with Generators

Problem Description:
LLM providers (like OpenAI, Anthropic, Gemini) support streaming, allowing tokens to be sent 
to the client as they are generated. This improves perceived latency (time to first token).

Implement a generator-based streaming client/server simulator.
1. `mock_llm_stream_server(prompt: str, response_text: str, delay: float = 0.01) -> Generator[dict, None, None]`:
   Simulates an LLM server. It splits `response_text` into words (or characters) and yields
   structured JSON-like dictionary chunks with a small sleep delay.
   The structure of each yielded chunk should resemble:
   `{"id": "chatcmpl-123", "choices": [{"delta": {"content": "word_here"}}], "done": False}`
   The last chunk should yield `{"choices": [], "done": True}`.

2. `stream_consumer(stream_generator) -> tuple[str, int]`:
   Consumes the generator stream, prints the text chunk-by-chunk to the stdout (using `print(..., end="", flush=True)`),
   and returns a tuple containing the full reconstructed string and the total number of chunks received.
"""

import time
from typing import Generator, Tuple

def mock_llm_stream_server(
    prompt: str, 
    response_text: str, 
    delay: float = 0.01
) -> Generator[dict, None, None]:
    """
    Simulates a streaming API endpoint. Yields dict chunks of the response text over time.
    """
    # Split by spaces but preserve space by appending it to the words
    words = response_text.split(" ")
    
    for idx, word in enumerate(words):
        # Add the space back to everything except the last word
        content = word if idx == len(words) - 1 else word + " "
        
        # Yield the chunk
        yield {
            "id": f"chatcmpl-{idx}",
            "choices": [{"delta": {"content": content}}],
            "done": False
        }
        time.sleep(delay)
        
    # Final terminator chunk
    yield {
        "id": "chatcmpl-final",
        "choices": [],
        "done": True
    }

def stream_consumer(stream_generator: Generator[dict, None, None]) -> Tuple[str, int]:
    """
    Consumes the mock stream, prints content in real-time, and aggregates the response.
    """
    reconstructed_text = []
    chunk_count = 0
    
    for chunk in stream_generator:
        chunk_count += 1
        
        if chunk.get("done") is True:
            break
            
        choices = chunk.get("choices", [])
        if choices:
            delta = choices[0].get("delta", {})
            content = delta.get("content", "")
            if content:
                print(content, end="", flush=True)
                reconstructed_text.append(content)
                
    print()  # Add trailing newline after stream finishes
    return "".join(reconstructed_text), chunk_count

# --- Verification Tests ---
if __name__ == "__main__":
    print("Running tests for Streaming API...")
    
    prompt = "Tell me a joke."
    response = "Why don't scientists trust atoms? Because they make up everything!"
    
    print("Streaming output: ", end="")
    # Create the generator stream
    stream = mock_llm_stream_server(prompt, response, delay=0.005)
    
    # Consume the stream
    full_text, chunks = stream_consumer(stream)
    
    print(f"Total chunks processed: {chunks}")
    print(f"Reconstructed output: '{full_text}'")
    
    assert full_text == response, "Reconstructed text did not match the original response!"
    assert chunks > 1, "Expected streaming to yield multiple chunks."
    
    print("All tests passed successfully!")
