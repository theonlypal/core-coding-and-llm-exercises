# Core Coding and LLM Engineering Exercises

This repository is split into five sections:
1. **Core Coding**: Classic data structure and algorithm (DSA) questions commonly tested in technical screens.
2. **LLM Coding**: Production-grade engineering challenges focused on working with large language models, streaming, tokenization, embeddings, vector databases, rate limits, concurrency, and validation.
3. **AI Engineering**: End-to-end practical pipelines for key AI systems, including RAG pipelines, chatbots, agents, OCR extraction, and local code assistants.
4. **Advanced AI Engineering**: High-level production AI patterns, including Paged Attention KV Caching, Hybrid Search (BM25 + Vector RRF), Multi-Agent DAGs, Guardrails/PII Redaction, Reflexion self-correction loops, and Speculative Decoding acceleration.
5. **AI System Architecture**: Systems-level AI engineering components, including Guided Decoding Logit Masking, GraphRAG, Auto Tool Schema Generators, MemGPT Tiered Memory, OpenTelemetry Tracing, Semantic Chunking, Context Compression, Streaming JSON Parsers, Load Balancing/Failover, and Prompt Security Shields.

---

## Directory Structure

### 1. Core Coding (`core_coding/`)
Each file includes the problem description, target complexity, templates, and self-verifying test cases:
*   [01_arrays_and_hashmaps.py](core_coding/01_arrays_and_hashmaps.py) — **Group Anagrams** (LeetCode 49)
*   [02_strings.py](core_coding/02_strings.py) — **Valid Palindrome** (LeetCode 125)
*   [03_trees.py](core_coding/03_trees.py) — **Binary Tree Traversal** (DFS: Max Depth, BFS: Level Order)
*   [04_graphs.py](core_coding/04_graphs.py) — **Number of Islands** (LeetCode 200)
*   [05_heaps.py](core_coding/05_heaps.py) — **Kth Largest Element in an Array** (LeetCode 215)
*   [06_binary_search.py](core_coding/06_binary_search.py) — **Search in Rotated Sorted Array** (LeetCode 33)
*   [07_sliding_window.py](core_coding/07_sliding_window.py) — **Longest Substring Without Repeating Characters** (LeetCode 3)
*   [08_dynamic_programming.py](core_coding/08_dynamic_programming.py) — **Coin Change** (LeetCode 322)
*   [09_backtracking.py](core_coding/09_backtracking.py) — **Generate Parentheses** (LeetCode 22)

### 2. LLM Coding (`llm_coding/`)
Practical, self-contained AI-native backend challenges implemented in pure Python:
*   [01_token_counting.py](llm_coding/01_token_counting.py) — **Byte-Pair Encoding (BPE) Tokenizer**: Merges frequencies and counts tokens.
*   [02_text_chunker.py](llm_coding/02_text_chunker.py) — **Recursive Character Text Splitter**: Chunks text with overlap boundaries.
*   [03_embedding_cache.py](llm_coding/03_embedding_cache.py) — **Thread-Safe Semantic Cache**: Bypasses LLM calls using cosine similarity.
*   [04_simple_vector_db.py](llm_coding/04_simple_vector_db.py) — **Simple In-Memory Vector DB**: Supports Cosine and Euclidean search.
*   [05_cosine_similarity.py](llm_coding/05_cosine_similarity.py) — **Cosine Similarity Engine**: Handles edge cases (zero vectors, dimensions).
*   [06_prompt_templates.py](llm_coding/06_prompt_templates.py) — **Prompt Template Engine**: Validates variables and formats chat structures.
*   [07_streaming_api.py](llm_coding/07_streaming_api.py) — **Mock LLM Streaming API**: Generator server and console stream consumer.
*   [08_rate_limiter.py](llm_coding/08_rate_limiter.py) — **Token Bucket Rate Limiter**: Thread-safe RPM/TPM control.
*   [09_exponential_backoff.py](llm_coding/09_exponential_backoff.py) — **Exponential Backoff Decorator**: Automatic retries with randomized jitter.
*   [10_parallel_llm_calls.py](llm_coding/10_parallel_llm_calls.py) — **Concurrent LLM Batch Processor**: Thread pool execution with safety limits.
*   [11_json_schema_validation.py](llm_coding/11_json_schema_validation.py) — **LLM JSON Schema Validator**: Validates structured output, auto-casts types.

### 3. AI Engineering (`ai_engineering/`)
Complete pipeline implementations for production AI services:
*   [01_rag_pipeline.py](ai_engineering/01_rag_pipeline.py) — **Mini RAG Pipeline**: Chunking, Term-Frequency embeddings, cosine vector search, context retrieval, and dynamic prompt assembly.
*   [02_ai_chatbot.py](ai_engineering/02_ai_chatbot.py) — **AI Chatbot**: Conversation memory storage, token streaming generator, auto-tool calling (time/math), and structured output formatting.
*   [03_agent.py](ai_engineering/03_agent.py) — **Autonomous ReAct Agent**: Reasoning loop orchestrator utilizing thought-action-observation cycles and tool execution.
*   [04_ocr_pipeline.py](ai_engineering/04_ocr_pipeline.py) — **Scanned Document Extraction**: OCR character error cleanup, regex parsing for dates/invoices/amounts, and validation cleanups.
*   [05_coding_assistant.py](ai_engineering/05_coding_assistant.py) — **Local Codebase Assistant**: Repository file and function index mapping, code symbol keyword querying, and automated code block injection.

### 4. Advanced AI Engineering (`advanced_ai_engineering/`)
Advanced production AI architecture and performance optimizations:
*   [01_kv_cache_simulator.py](advanced_ai_engineering/01_kv_cache_simulator.py) — **KV Cache Simulator**: Block memory allocation for Paged Attention and memory savings calculation.
*   [02_semantic_router.py](advanced_ai_engineering/02_semantic_router.py) — **Semantic Router**: Exemplar embedding distance calculation and dynamic intent route dispatching.
*   [03_hybrid_search_rrf.py](advanced_ai_engineering/03_hybrid_search_rrf.py) — **Hybrid Search RRF**: BM25 keyword matching + Cosine vector search combined using Reciprocal Rank Fusion ($RRF\_Score = \sum \frac{1}{k + rank}$).
*   [04_multi_agent_dag.py](advanced_ai_engineering/04_multi_agent_dag.py) — **Multi-Agent DAG**: Directed Acyclic Graph topology sorting and state orchestration.
*   [05_guardrails_pii_redactor.py](advanced_ai_engineering/05_guardrails_pii_redactor.py) — **Guardrails & PII Redactor**: Pattern redaction (emails, SSNs, phone numbers) and prompt injection defense.
*   [06_long_context_summarizer.py](advanced_ai_engineering/06_long_context_summarizer.py) — **Long-Context Summarizer**: Parallel Map-Reduce and sequential Refine summarization algorithms.
*   [07_fine_tuning_dataset_generator.py](advanced_ai_engineering/07_fine_tuning_dataset_generator.py) — **Fine-Tuning Dataset Generator**: Instruction-Input-Output schema validation, similarity deduplication, and JSONL export.
*   [08_llm_evaluator_metrics.py](advanced_ai_engineering/08_llm_evaluator_metrics.py) — **LLM Evaluator Metrics**: ROUGE-1 / ROUGE-L n-gram overlap algorithms and LLM-as-a-Judge Faithfulness scoring.
*   [09_self_correction_reflexion.py](advanced_ai_engineering/09_self_correction_reflexion.py) — **Reflexion Self-Correction**: Isolated execution environment, exception capture, and iterative code healing loop.
*   [10_speculative_decoding.py](advanced_ai_engineering/10_speculative_decoding.py) — **Speculative Decoding**: Draft model candidate token verification and generation speedup calculation.

### 5. AI System Architecture (`system_architecture/`)
Systems-level AI components and production safeguards:
*   [01_guided_decoding_masker.py](system_architecture/01_guided_decoding_masker.py) — **Guided Decoding Masker**: FSM logit masking setting invalid token logits to `-inf` to guarantee valid syntax.
*   [02_graph_rag_triples.py](system_architecture/02_graph_rag_triples.py) — **GraphRAG Triples**: Subject-predicate-object extraction, Knowledge Graph construction, and multi-hop neighborhood retrieval.
*   [03_tool_schema_generator.py](system_architecture/03_tool_schema_generator.py) — **Auto Tool Schema Generator**: Function signature reflection auto-generating OpenAI/Anthropic tool JSON schemas.
*   [04_tiered_agent_memory.py](system_architecture/04_tiered_agent_memory.py) — **Tiered Agent Memory**: MemGPT-style Working, Episodic, and Archived memory management.
*   [05_llm_tracer_telemetry.py](system_architecture/05_llm_tracer_telemetry.py) — **LLM Tracer Telemetry**: OpenTelemetry-style span tree tracing, latency timing, and token counting.
*   [06_semantic_chunker.py](system_architecture/06_semantic_chunker.py) — **Semantic Chunker**: Splitting text at high sentence embedding distance boundaries.
*   [07_context_compression.py](system_architecture/07_context_compression.py) — **Context Compression**: Stop-word filtering and relevance-based sentence extraction fitting within token limits.
*   [08_streaming_json_parser.py](system_architecture/08_streaming_json_parser.py) — **Streaming Partial JSON Parser**: Auto-completing unclosed quotes, brackets, and braces on partial token streams.
*   [09_model_fallback_load_balancer.py](system_architecture/09_model_fallback_load_balancer.py) — **Model Load Balancer & Fallback**: Round-robin provider balancing and automated priority chain failover.
*   [10_prompt_security_shield.py](system_architecture/10_prompt_security_shield.py) — **Prompt Security Shield**: Escaping XML tags in user inputs and enforcing structural boundary rules.

---

## Author & Contact
- **Name**: Rayan Pal
- **GitHub**: [theonlypal](https://github.com/theonlypal)
- **Email**: rpal@sandiego.edu
