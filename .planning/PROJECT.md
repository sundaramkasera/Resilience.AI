# Resilience.AI

## What This Is

Resilience.AI is a smart city emergency command center prototype acting as a "War Room" dashboard for managing a macro-city grid. It leverages a graph database (TigerGraph) for infrastructure topology and multi-agent AI (LangChain/Groq) to identify Single Points of Failure (SPOF), evaluate blast radii, and simulate weather impacts dynamically.

## Core Value

Real-time, deterministic, and accurate situational awareness of the city grid's health and vulnerabilities under emergency scenarios.

## Requirements

### Validated

- ✓ Interactive Streamlit dashboard with chat UI and live telemetry components.
- ✓ PyDeck geospatial map rendering of graph nodes (Substations, Hospitals, Towers, etc.) and edges.
- ✓ Multi-agent system architecture (Power Grid Agent, Logistics Agent, Commander Agent).
- ✓ Basic TigerGraph Cloud connection and query capability.

### Active

- [ ] Eliminate Arbitrary Code Execution (RCE) by replacing `exec()` with explicit, parameterized LangChain `@tool`s.
- [ ] Secure hardcoded credentials by migrating them to `.env` variables.
- [ ] Enforce deterministic structured LLM output (Pydantic `SimulationResponse`) instead of regex JSON parsing.
- [ ] Resolve file concurrency issues on `telemetry_stream.json` via atomic writes (`filelock` or `os.replace`).
- [ ] Implement robust exception handling and exponential backoff retries for TigerGraph connections.
- [ ] Optimize PyDeck map performance by separating static infrastructure layers from dynamic outage layers (in-memory filtering vs database querying).

### Out of Scope

- [ ] Modifying the underlying model stack (must keep `qwen/qwen3.6-27b` with `openai/gpt-oss-20b` fallback).
- [ ] Altering the existing graph schema (vertex types and edge semantics remain unchanged).
- [ ] Changing the UI aesthetic (must maintain the `CARTO_DARK` theme and `@st.fragment` architecture).

## Context

The project recently passed an automated code audit (`concerns.md`). The audit revealed critical security vulnerabilities (RCE via `exec()`), brittle JSON regex extraction, hardcoded secrets, read/write race conditions on the telemetry stream, and performance bottlenecks in the PyDeck map rendering due to blocking sleep loops and excessive edge re-requesting.

## Constraints

- **Tech Stack**: Must remain entirely in Python, utilizing Streamlit, LangChain, PyDeck, and pyTigerGraph.
- **Security**: Must strictly follow zero-trust execution; the LLM cannot run arbitrary Python code.
- **Performance**: Real-time map rendering must achieve sub-second updates without blocking the main event loop.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Deprecate dynamic `exec()` for explicit parameterized tools | Stops RCE vulnerability and forces deterministic, structured logic. | — Pending |
| Adopt LangChain `.with_structured_output` | Fixes the brittle regex parsing and guarantees expected fields (`affected_nodes`, `spof_node`). | — Pending |
| Implement two-layer PyDeck rendering | Eliminates the `time.sleep(0.05)` bottleneck and reduces TigerGraph load. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-10-06 after initialization*
