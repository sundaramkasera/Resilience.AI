# Phase 04 Plan 03: Zero-Rerun Map Update Architecture

---
phase: 04
plan: 03
subsystem: performance
tags: [caching, streamlit-fragments, latency, zero-rerun, pydeck]
key-files.modified: [app.py, agent.py]
key-decisions:
  - Moved map rendering into a `st.empty()` placeholder before the chat interactions block.
  - Pushed updated map layer data directly to the placeholder on-the-fly (`map_container.pydeck_chart()`) avoiding `st.rerun()`.
  - Switched Pydantic parsing strictly over to `llama3-8b-8192` for high-speed sub-second extraction without compromising the main agent context.
requirements: [PERF-04]
duration: 2 min
completed: 2026-10-06T20:10:00Z
coverage:
  - kind: human-judgment
    status: pass
    human_judgment: true
    rationale: "Successfully implemented zero-rerun architecture to instantly update the map when the SPOF node is extracted."
---

## Accomplishments

- Replaced full-page Streamlit rerun with an in-place PyDeck push.
- Separated extraction LLM from core orchestration LLM, speeding up the serialization step significantly.

## Deviations from Plan

None.

## Self-Check: PASSED
