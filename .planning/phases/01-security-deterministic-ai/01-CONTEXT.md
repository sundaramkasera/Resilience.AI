# Phase 1: Security & Deterministic AI - Context

**Gathered:** 2026-10-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Secure the agent execution environment, sanitize credentials, and migrate to deterministic typed LLM responses.
</domain>

<decisions>
## Implementation Decisions

### Environment Variable Loading
- **D-01:** Explicitly call `load_dotenv()` in `app.py`. — **Reversibility:** reversible — simplifies local development and ensures `.env` is loaded reliably without complex runner configuration.

### LangChain Tool Error Handling
- **D-02:** Tools must return formatted error strings (e.g., JSON error objects) to the LLM instead of raising exceptions that halt the UI. — **Reversibility:** costly — changes the contract of all tools and requires the LLM prompt/agent loop to handle error correction gracefully.

### SPOF Fallback Behavior
- **D-03:** The UI should fail silently (no highlighting) if the LLM hallucinates an invalid node ID. — **Reversibility:** reversible — requires a simple validation check before rendering the overlay.

### LLM Model Fallback
- **D-04:** Use LangChain's native `.with_fallbacks()` for seamless, automatic failover from `qwen3.6-27b` to `openai/gpt-oss-20b` without user intervention. — **Reversibility:** costly — alters the LangChain initialization and invocation pipeline across the app.

### the agent's Discretion
None explicitly stated. Use standard Python best practices for the `.env.example` template structure.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Audits & Constraints
- `.planning/codebase/CONCERNS.md` — Security audit findings and RCE vulnerability details
- `.planning/codebase/ARCHITECTURE.md` — Existing system architecture and component interactions

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app.py`: Contains the main Streamlit interface and `agent_executor` invocation logic.
- `tigergraph_client.py`: Centralized database connection logic.
- `agent.py`: Contains existing prompts and the `execute_dynamic_python` block that must be removed.

### Established Patterns
- Streamlit state management via `st.session_state`
- LangChain multi-agent graph/orchestration structure
- PyDeck rendering mapped to `st.fragment`

### Integration Points
- Connecting LangChain tools natively to the agent orchestrator in `agent.py`.
- Passing the validated `.with_structured_output` response down to `app.py` for map state updates.

</code_context>

<specifics>
## Specific Ideas

No specific UI visual requirements added; the change is primarily structural (replacing regex parsing with Pydantic schemas) and security-focused (removing `exec()`).

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.
</deferred>

---

*Phase: 1-Security & Deterministic AI*
*Context gathered: 2026-10-06*
