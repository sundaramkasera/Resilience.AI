# 01-02: Implement explicit LangChain tools and remove `execute_dynamic_python` (`exec()`)

## Summary of Changes
- Removed the `execute_dynamic_python` tool and its `exec()` call from `agent.py`.
- Added 3 explicit deterministic tools: `calculate_blast_radius`, `find_single_point_of_failure`, and `route_emergency_logistics`.
- The tools now return JSON-formatted error strings instead of throwing exceptions.
- Updated the Power Grid Agent and Logistics Agent prompts to explain how to use the new explicit tools.
- Bound the new explicit tools to the agent tool lists (`tg_tools`).

## Status
Completed successfully.
