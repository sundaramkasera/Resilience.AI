# Phase 2: Concurrency & Performance Optimization - Context

**Gathered:** 2026-10-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Ensure sub-second, non-blocking map rendering and atomic state telemetry.
</domain>

<decisions>
## Implementation Decisions

### Telemetry File Locking
- **D-01:** `os.replace` (atomic rename, zero dependencies) — **Reversibility:** reversible — requires creating a temp file and swapping it atomically, avoids introducing pip dependencies.

### TigerGraph Error Surfacing
- **D-02:** `st.toast()` - Subtle notification — **Reversibility:** reversible — prevents intrusive blocking errors and allows users to continue interacting with the LLM chat while connections retry.

### Map Rendering Separation
- **D-03:** Pre-render static layer and overlay a dynamic outages layer (uses `@st.cache_data` for static graph) — **Reversibility:** costly — changes the PyDeck structural rendering logic from a single pass to a multi-layer composition, but drastically improves frame rates.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Audits & Constraints
- `.planning/codebase/CONCERNS.md` — Security audit findings and performance bottlenecks.
- `.planning/codebase/ARCHITECTURE.md` — Existing system architecture and component interactions.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `telemetry_stream.json`: The live feed file to lock.
- `graph_renderer.py`: The map rendering logic to split into cached static + dynamic layers.
- `get_tg_connection()`: The database connection logic to refactor for retries.

### Established Patterns
- Streamlit `st.session_state` management for persisting offline nodes.
- `@st.fragment` used for localized rendering without full app reruns.

### Integration Points
- Connecting the new TigerGraphConnectionError exceptions to Streamlit's `st.toast()` UI mechanism.
- Rewiring `app.py` to call the cached static layer generator in `graph_renderer.py`.

</code_context>

<specifics>
## Specific Ideas
- N/A
</specifics>

<deferred>
## Deferred Ideas
None
</deferred>
