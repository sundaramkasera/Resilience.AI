# 01-03: Implement `SimulationResponse` schema and `.with_structured_output()`

## Summary of Changes
- Defined `SimulationResponse` Pydantic schema in `agent.py` to structure outputs with `summary`, `spof_node`, `affected_nodes`, and `logistics_routes`.
- Modified the Commander Agent (`get_resilience_agent()`) to pipe the output text through `.with_structured_output(SimulationResponse)`, guaranteeing deterministic JSON parsing.
- Refactored `app.py` to remove legacy regex-based JSON extraction (`re.search(r'\{.*\}', ...)`) and instead consume the `SimulationResponse` object directly.
- Added validation logic to fail silently and avoid crashing the PyDeck highlight overlay if a `spof_node` or `affected_nodes` array is empty or invalid.
- Retained the `with_fallbacks()` logic as originally configured in `agent.py`.

## Status
Completed successfully.
