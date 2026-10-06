# Requirements: Resilience.AI

**Defined:** 2026-10-06
**Core Value:** Real-time, deterministic, and accurate situational awareness of the city grid's health and vulnerabilities under emergency scenarios.

## v1 Requirements

### Security

- [ ] **SECR-01**: Remove `execute_dynamic_python` and any usage of Python's built-in `exec()` in `agent.py`.
- [ ] **SECR-02**: Remove plain-text passwords and secrets from `tigergraph_client.py`.
- [ ] **SECR-03**: Initialize connections strictly via environment variables using `os.getenv()` and `python-dotenv` (`TG_HOST`, `TG_GRAPH`, `TG_USERNAME`, `TG_PASSWORD`, `TG_SECRET`).
- [ ] **SECR-04**: Create a sanitized `.env.example` template with configuration placeholders.

### Deterministic AI

- [ ] **DAI-01**: Implement explicit, parameterized LangChain tools (`calculate_blast_radius`, `find_single_point_of_failure`, `route_emergency_logistics`).
- [ ] **DAI-02**: Bind the new tools directly to the Power Grid and Logistics agents.
- [ ] **DAI-03**: Define `SimulationResponse` Pydantic schema (`summary`, `spof_node`, `affected_nodes`, `logistics_routes`).
- [ ] **DAI-04**: Configure the agent workflow to use LangChain's `.with_structured_output(SimulationResponse)`.
- [ ] **DAI-05**: Refactor `app.py` to consume the typed `SimulationResponse` and completely eliminate regex JSON parsing.

### Concurrency

- [ ] **CONC-01**: Implement atomic write strategy (via `filelock` or `os.replace`) for `telemetry_stream.json`.
- [ ] **CONC-02**: Eliminate unsynchronized read/write race conditions between `telemetry_simulator.py` and `app.py`.

### Performance & Reliability

- [ ] **PERF-01**: Refactor `get_tg_connection()` to remove silent catch-all exception swallowing.
- [ ] **PERF-02**: Implement custom `TigerGraphConnectionError` with 3-attempt exponential backoff retries.
- [ ] **PERF-03**: Handle connection failures explicitly in `app.py` using `st.error()` or `st.toast()`.
- [ ] **PERF-04**: Decouple PyDeck rendering into a cached Static Infrastructure Layer (`@st.cache_data`) and a dynamic in-memory Outage Layer.
- [ ] **PERF-05**: Eliminate `time.sleep()` loops and artificial vertex slicing in map rendering by using batch graph retrieval.

## v2 Requirements

*(None yet)*

## Out of Scope

| Feature | Reason |
|---------|--------|
| Model Swap | Current implementation relies on `qwen3.6-27b` via Groq. Changing models introduces latency regressions. |
| Schema Changes | Current TigerGraph schema covers all semantic requirements for routing and grid traversal. |
| UI Redesign | The `CARTO_DARK` PyDeck theme and `@st.fragment` architecture are mandatory for current user expectations. |

## Traceability

*(To be populated during roadmap creation)*

| Requirement | Phase | Status |
|-------------|-------|--------|
| SECR-01 | Phase 1 | Pending |
| SECR-02 | Phase 1 | Pending |
| SECR-03 | Phase 1 | Pending |
| SECR-04 | Phase 1 | Pending |
| DAI-01 | Phase 1 | Pending |
| DAI-02 | Phase 1 | Pending |
| DAI-03 | Phase 1 | Pending |
| DAI-04 | Phase 1 | Pending |
| DAI-05 | Phase 1 | Pending |
| CONC-01 | Phase 2 | Pending |
| CONC-02 | Phase 2 | Pending |
| PERF-01 | Phase 2 | Pending |
| PERF-02 | Phase 2 | Pending |
| PERF-03 | Phase 2 | Pending |
| PERF-04 | Phase 2 | Pending |
| PERF-05 | Phase 2 | Pending |

**Coverage:**
- v1 requirements: 16 total
- Mapped to phases: 16
- Unmapped: 0 ✓

---
*Requirements defined: 2026-10-06*
*Last updated: 2026-10-06 after initial definition*
