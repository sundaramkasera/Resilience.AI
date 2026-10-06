# Phase 1: Security & Deterministic AI - Research

**Date:** 2026-10-06

## 1. Context & Goals
The goal of this phase is to secure the agent execution environment, sanitize credentials, and migrate to deterministic typed LLM responses. We will eliminate Arbitrary Code Execution (RCE) in `agent.py`, move secrets to `.env`, and implement `SimulationResponse` using LangChain's structured output.

## 2. Technical Approach
- **Environment Variables**: Create `.env.example` and load via `dotenv` in `app.py`. Update `tigergraph_client.py` to use `os.getenv()`.
- **LangChain Tools**: Refactor `agent.py` to replace `execute_dynamic_python` with explicit `@tool` decorated functions: `calculate_blast_radius`, `find_single_point_of_failure`, `route_emergency_logistics`.
- **Structured Output**: Define `SimulationResponse` in `agent.py` using Pydantic. Update the LLM call to use `.with_structured_output(SimulationResponse)`.
- **Error Handling**: Tools will return formatted error JSON strings to the LLM.
- **Model Fallback**: Implement LangChain `.with_fallbacks()` for failover from `qwen3.6-27b` to `openai/gpt-oss-20b`.

## 3. Risks & Dependencies
- LangChain API versions might affect `.with_structured_output()` and `.with_fallbacks()`.
- TigerGraph client initialization assumes the host and secrets are passed securely.

## 4. Validation Architecture
Not enabled for this phase.
