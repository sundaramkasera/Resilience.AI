# Project Research Summary

**Project:** Resilience.AI
**Domain:** Smart city emergency command center / Graph + LLM integration
**Researched:** 2026-10-06
**Confidence:** HIGH

## Executive Summary

Resilience.AI operates as a macro-city emergency command center prototype. Current research indicates that managing this level of geospatial and topological infrastructure effectively demands robust LLM grounding. The existing stack (Streamlit, PyDeck, TigerGraph, LangChain, Groq) is sufficient for real-time visualization and complex relationship traversal.

The recommended approach enforces determinism through explicit, typed LangChain tools rather than arbitrary `exec()` code. Furthermore, separating static topology from dynamic state enables significant performance optimization for PyDeck map rendering.

## Key Findings

### Recommended Stack

The established stack is highly suited for this domain, but requires modernization of its integration patterns.

**Core technologies:**
- **LangChain/Groq (`qwen3.6-27b`)**: Orchestration & intelligence — powerful enough for structured output (`.with_structured_output`) and tool binding.
- **TigerGraph & pyTigerGraph**: Graph DB — critical for infrastructure topology (`POWERS`, `CONNECTS_TO` edges).
- **Streamlit & PyDeck**: Visualization — effective for geospatial rendering if layered properly via caching.
- **python-dotenv**: Security — industry standard for environment variable management.
- **filelock**: Concurrency — guarantees atomic writes on the telemetry stream.

### Expected Features

**Must have (table stakes):**
- Secure, parameterized AI tool calling (no RCE vulnerabilities).
- Real-time map updates (sub-second rendering).
- Deterministic AI outputs (structured JSON without regex parsing).
- Secure credential management.

### Architecture Approach

**Major components:**
1. **Tool-Driven Orchestrator**: LangChain agents bound to strict tools (`calculate_blast_radius`, `find_single_point_of_failure`, `route_emergency_logistics`).
2. **Layered Renderer**: A static PyDeck base layer (cached) combined with an in-memory dynamic outage overlay.
3. **Atomic State Manager**: File locks securing `telemetry_stream.json` to prevent race conditions during updates.

### Critical Pitfalls

1. **Arbitrary Code Execution (RCE)** — Passing generated code directly to `exec()` is an immediate blocker and massive vulnerability. Avoid by parameterizing LLM calls.
2. **Blocking UI / Sleep Loops** — Adding `time.sleep()` for sequential edge fetching stalls Streamlit. Avoid by fetching batches and managing state asynchronously.
3. **Regex Fragility** — Using regex for LLM JSON parsing breaks frequently. Avoid by using strictly typed `Pydantic` schemas natively.
4. **Swallowed Exceptions** — Catch-all exception handling in DB connections hides critical network issues. Use specific exception handling with exponential backoff.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Security & Deterministic AI
**Rationale:** Fixes severe RCE vulnerability, secret leakage, and brittle regex parsing.
**Delivers:** Parameterized tools, `SimulationResponse` Pydantic schema, `.env` file implementation.
**Addresses:** Security requirements, deterministic LLM output.
**Avoids:** RCE and regex fragility pitfalls.

### Phase 2: Concurrency & Performance Optimization
**Rationale:** Necessary for real-time dashboard stability and sub-second rendering.
**Delivers:** Atomic writes via `filelock`, layered PyDeck rendering (static cached vs dynamic), robust connection retries.
**Uses:** `filelock`, Streamlit caching (`@st.cache_data`).
**Implements:** High-performance rendering pipeline.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Validated against existing `ARCHITECTURE.md` |
| Features | HIGH | Directly sourced from project context |
| Architecture | HIGH | Established patterns in LangChain and Streamlit |
| Pitfalls | HIGH | Identified via security audits |

**Overall confidence:** HIGH

## Sources

### Primary (HIGH confidence)
- Project codebase audit (`concerns.md`)
- LangChain Official Documentation — Tool calling and `.with_structured_output`
- Streamlit Documentation — Caching and session state performance
- TigerGraph SDK patterns

---
*Research completed: 2026-10-06*
*Ready for roadmap: yes*
