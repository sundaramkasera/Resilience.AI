# Roadmap: Resilience.AI

## Overview

This roadmap defines the immediate stabilization efforts for the Resilience.AI prototype, breaking down the work into two prioritized phases. Phase 1 focuses on eliminating critical security vulnerabilities (RCE, hardcoded secrets) and enforcing deterministic AI outputs. Phase 2 focuses on resolving concurrency bottlenecks and optimizing geospatial map rendering for real-time responsiveness.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Security & Deterministic AI** - Eliminate RCE, secure credentials, and enforce structured outputs.
- [ ] **Phase 2: Concurrency & Performance Optimization** - Fix telemetry race conditions and optimize PyDeck map rendering.

## Phase Details

### Phase 1: Security & Deterministic AI

**Goal**: Secure the agent execution environment, sanitize credentials, and migrate to deterministic typed LLM responses.
**Depends on**: Nothing (first phase)
**Requirements**: SECR-01, SECR-02, SECR-03, SECR-04, DAI-01, DAI-02, DAI-03, DAI-04, DAI-05
**Success Criteria** (what must be TRUE):
  1. `execute_dynamic_python` and `exec()` are entirely removed from the codebase.
  2. TigerGraph credentials are read strictly from `.env`.
  3. The LLM agent returns structured `SimulationResponse` objects; regex extraction is removed.

**Plans**: 3 plans

Plans:
- [x] 01-01: Remove hardcoded credentials and implement `.env` configuration.
- [x] 01-02: Implement explicit LangChain tools and remove `execute_dynamic_python` (`exec()`).
- [x] 01-03: Implement `SimulationResponse` schema and `.with_structured_output()`.

### Phase 2: Concurrency & Performance Optimization

**Goal**: Ensure sub-second, non-blocking map rendering and atomic state telemetry.
**Depends on**: Phase 1
**Requirements**: CONC-01, CONC-02, PERF-01, PERF-02, PERF-03, PERF-04, PERF-05
**Success Criteria** (what must be TRUE):
  1. `telemetry_stream.json` writes do not crash or corrupt active reads in Streamlit.
  2. TigerGraph connection failures surface visibly in the UI and automatically retry.
  3. Map rendering does not block on `time.sleep()`, using separate static and dynamic layers.

**Plans**: 1/3 plans executed

Plans:
- [x] 02-01: Implement `filelock` for atomic writes on `telemetry_stream.json`.
- [ ] 02-02: Implement exponential backoff retries and UI error surfacing for TigerGraph connections.
- [ ] 02-03: Refactor PyDeck map rendering into static cache and dynamic memory layers.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Security & Deterministic AI | 3/3 | Complete | 2026-10-06 |
| 2. Concurrency & Performance | 1/3 | In Progress | - |
